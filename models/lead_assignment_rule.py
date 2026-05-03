from odoo import models, fields


class LeadAssignmentRule(models.Model):
    _name = 'lead.assignment.rule'
    _description = 'Lead Assignment Rule'
    _order = 'sequence asc'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10, help='Lower = checked first.')
    active = fields.Boolean(default=True)

    # Match conditions (ALL must apply for the rule to win)
    country_ids = fields.Many2many('res.country', string='Countries (any of)')
    min_expected_revenue = fields.Float(default=0.0)
    min_lead_score = fields.Integer(default=0)
    tag_ids = fields.Many2many('crm.tag', string='Tags (any of)')

    # Assignment target
    user_id = fields.Many2one('res.users', string='Assign to', required=True)
    team_id = fields.Many2one('crm.team', string='Sales Team')

    def matches(self, lead):
        '''Return True if all conditions on this rule pass for the given lead.'''
        self.ensure_one()
        if self.country_ids and lead.country_id not in self.country_ids:
            return False
        if (lead.expected_revenue or 0) < self.min_expected_revenue:
            return False
        if (lead.lead_score or 0) < self.min_lead_score:
            return False
        if self.tag_ids and not (self.tag_ids & lead.tag_ids):
            return False
        return True