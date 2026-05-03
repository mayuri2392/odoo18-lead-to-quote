from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # --- existing fields from Phase 4 ---
    lead_score = fields.Integer(
        string='Lead Score',
        compute='_compute_lead_score',
        store=True,
        help='0-100 computed from active scoring rules. Higher = hotter.'
    )

    score_band = fields.Selection([
        ('cold', 'Cold'),
        ('warm', 'Warm'),
        ('hot', 'Hot'),
    ], compute='_compute_score_band', store=True)

    # --- NEW Phase 6 fields ---
    auto_assigned = fields.Boolean(
        string='Auto-assigned',
        help='True if a salesperson was set by an assignment rule.'
    )
    assignment_rule_id = fields.Many2one(
        'lead.assignment.rule',
        string='Assignment Rule',
        readonly=True,
    )

    # --- existing computes from Phase 4 ---
    @api.depends('expected_revenue', 'probability', 'country_id', 'tag_ids', 'source_id')
    def _compute_lead_score(self):
        rules = self.env['lead.scoring.rule'].search([('active', '=', True)])
        for lead in self:
            total = 0
            for rule in rules:
                total += rule.apply(lead)
            lead.lead_score = min(max(total, 0), 100)

    @api.depends('lead_score')
    def _compute_score_band(self):
        for lead in self:
            if lead.lead_score >= 70:
                lead.score_band = 'hot'
            elif lead.lead_score >= 40:
                lead.score_band = 'warm'
            else:
                lead.score_band = 'cold'

    # --- NEW Phase 6 methods ---
    @api.model_create_multi
    def create(self, vals_list):
        leads = super().create(vals_list)
        for lead in leads:
            lead._auto_assign_salesperson()
        return leads

    def _auto_assign_salesperson(self):
        '''Run active assignment rules in sequence order. First match wins.'''
        rules = self.env['lead.assignment.rule'].search(
            [('active', '=', True)], order='sequence asc'
        )
        for rule in rules:
            if rule.matches(self):
                self.write({
                    'user_id': rule.user_id.id,
                    'team_id': rule.team_id.id or False,
                    'auto_assigned': True,
                    'assignment_rule_id': rule.id,
                })
                self.message_post(
                    body=f'Auto-assigned to {rule.user_id.name} '
                         f'by rule "{rule.name}" (score: {self.lead_score}).'
                )
                return

    def action_create_quotation(self):
        '''Open the quote-from-lead wizard for this lead.'''
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Quotation',
            'res_model': 'quote.from.lead.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_lead_id': self.id},
        }