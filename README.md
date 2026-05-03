# odoo18-lead-to-quote

Odoo 18 module: CRM lead scoring → auto-assignment → guided quotation wizard.

Built as a portfolio project demonstrating end-to-end Sales + CRM customisation
in Odoo 18 Community. Follows Odoo S.A. coding conventions throughout.

## What it does

| Feature | Detail |
|---|---|
| Lead Scoring | Configurable rules: revenue, probability, country, tags, source. Score 0-100. |
| Score Band | Cold / Warm / Hot badge on the lead form. |
| Auto-assignment | First-match rule assigns salesperson + team on lead creation. |
| Quotation Wizard | Pre-filled SO from lead data. Button hides after first quote. |

## Tech used

`ORM`, `QWeb`, `OWL 2`, `ir.actions.act_window`, `onchange`, `api.depends`,
`model_create_multi`, `sale_crm` native field reuse, Odoo 18 `invisible` syntax.

## Install

Requires Odoo 18 Community with `sale_crm` and `sale_management` installed.

```bash
./odoo-bin -c odoo.conf -i lead_to_quote
```

## Author

Mayuri Patil — Odoo Functional + Technical Consultant  
[LinkedIn](https://linkedin.com/in/mayuri-patil-2392) · [GitHub](https://github.com/mayuri2392)