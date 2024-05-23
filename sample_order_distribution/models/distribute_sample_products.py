from odoo import models, fields

class DistributeSampleProducts(models.Model):
    _name = 'distribute.sample.products'
    _description = 'Distribute Sample Products'

    item_no = fields.Integer(string='Item No', default=1)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    distribution_sample_order_id = fields.Many2one('distribution.sample.order', string='Distribution Sample Order')
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead')