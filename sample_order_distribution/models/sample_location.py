from odoo import models, fields, api, exceptions

class StockLocation(models.Model):
    _inherit = 'stock.location'

    is_sample_location = fields.Boolean(string='Is Sample Location')
    user_id = fields.Many2one('res.users', string='User')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    _sql_constraints = [
        ('unique_sample_location', 'unique(user_id, company_id, is_sample_location)', 'Each user can have only one sample location per company.')
    ]

    @api.model
    def create(self, vals):
        if vals.get('is_sample_location', False):
            existing_location = self.search([
                ('user_id', '=', vals.get('user_id')),
                ('company_id', '=', vals.get('company_id')),
                ('is_sample_location', '=', True)
            ], limit=1)
            if existing_location:
                raise exceptions.ValidationError("Sample location for this user already exists.")
        return super(StockLocation, self).create(vals)