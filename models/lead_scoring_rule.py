from odoo import models, fields, api


class LeadScoringRule(models.Model):
    _name = 'lead.scoring.rule'
    _description = 'Lead Scoring Rule'
    _order = 'sequence asc'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    condition_type = fields.Selection([
        ('min_revenue', 'Min. Expected Revenue'),
        ('has_tag', 'Has Tag'),
        ('country', 'From Country'),
        ('min_probability', 'Min. Probability'),
        ('source', 'From Source'),
    ], required=True)

    condition_value = fields.Char(
        help='For min_revenue and min_probability: a number. '
             'For other types, leave blank and use the matching field.'
    )
    tag_id = fields.Many2one('crm.tag')
    country_id = fields.Many2one('res.country')
    source_id = fields.Many2one('utm.source')

    points = fields.Integer(
        required=True, default=10,
        help='Points added to lead score when this rule matches.'
    )

    def apply(self, lead):
        '''Return points if rule matches, else 0.'''
        self.ensure_one()
        if self.condition_type == 'min_revenue':
            try:
                threshold = float(self.condition_value or 0)
            except ValueError:
                return 0
            return self.points if (lead.expected_revenue or 0) >= threshold else 0
        if self.condition_type == 'has_tag':
            return self.points if self.tag_id and self.tag_id in lead.tag_ids else 0
        if self.condition_type == 'country':
            return self.points if self.country_id and lead.country_id == self.country_id else 0
        if self.condition_type == 'min_probability':
            try:
                threshold = float(self.condition_value or 0)
            except ValueError:
                return 0
            return self.points if (lead.probability or 0) >= threshold else 0
        if self.condition_type == 'source':
            return self.points if self.source_id and lead.source_id == self.source_id else 0
        return 0