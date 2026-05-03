{
    'name': 'Lead to Quote',
    'version': '18.0.1.0.0',
    'summary': 'CRM lead scoring, auto-assignment, and one-click quote generation',
    'description': """
Lead to Quote
=============
- Configurable lead scoring rules (revenue, probability, country, tags, source)
- Auto-assignment of salesperson based on first-match rules
- Guided quotation wizard pre-filling product lines and pricing
- WhatsApp webhook stub for lead notification
    """,
    'author': 'Mayuri Patil',
    'website': 'https://github.com/mayuri2392',
    'category': 'Sales/CRM',
    'depends': ['crm', 'sale', 'sale_crm', 'sale_management', 'sales_team', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/assignment_rule_data.xml',
        'data/scoring_rule_data.xml',
        'views/scoring_rule_views.xml',
        'views/assignment_rule_views.xml',
        'views/crm_lead_views.xml',
        'wizard/quote_from_lead_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}