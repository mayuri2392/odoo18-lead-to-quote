from odoo import models, fields, api
from odoo.exceptions import UserError


class QuoteFromLeadWizard(models.TransientModel):
    _name = 'quote.from.lead.wizard'
    _description = 'Create Quotation from Lead'

    lead_id = fields.Many2one('crm.lead', required=True, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    create_partner_if_missing = fields.Boolean(default=True)
    product_line_ids = fields.One2many(
        'quote.from.lead.wizard.line', 'wizard_id',
        string='Product Lines'
    )
    validity_date = fields.Date(default=lambda self: fields.Date.context_today(self))
    note = fields.Text(string='Internal Note')

    @api.onchange('lead_id')
    def _onchange_lead_id(self):
        '''Pre-fill the customer from the lead if the lead already has one.'''
        if self.lead_id and self.lead_id.partner_id:
            self.partner_id = self.lead_id.partner_id

    def action_create_quote(self):
        '''Create a sale.order from the wizard, link it to the lead, return the SO form.'''
        self.ensure_one()
        partner = self.partner_id
        if not partner and self.create_partner_if_missing and self.lead_id:
            partner = self.env['res.partner'].create({
                'name': self.lead_id.contact_name or self.lead_id.partner_name or self.lead_id.name,
                'email': self.lead_id.email_from,
                'phone': self.lead_id.phone,
                'country_id': self.lead_id.country_id.id,
            })
            self.lead_id.partner_id = partner
        if not partner:
            raise UserError('Select or create a customer first.')

        order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'user_id': self.lead_id.user_id.id or self.env.user.id,
            'team_id': self.lead_id.team_id.id if self.lead_id.team_id else False,
            'validity_date': self.validity_date,
            'opportunity_id': self.lead_id.id,
            'note': self.note or '',
            'order_line': [
                (0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                })
                for line in self.product_line_ids
            ],
        })

        self.lead_id.message_post(body=f'Quotation {order.name} created from lead.')

        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'res_id': order.id,
            'view_mode': 'form',
        }


class QuoteFromLeadWizardLine(models.TransientModel):
    _name = 'quote.from.lead.wizard.line'
    _description = 'Quote Wizard Line'

    wizard_id = fields.Many2one('quote.from.lead.wizard')
    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Float(default=1.0, required=True)
    price_unit = fields.Float()

    @api.onchange('product_id')
    def _onchange_product(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price