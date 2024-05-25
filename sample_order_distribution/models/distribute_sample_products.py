from odoo import models, fields, api
class DistributeSampleProducts(models.Model):
    _name = 'distribute.sample.products'
    _description = 'Distribute Sample Products'

    item_no = fields.Integer(string='Item No', default=1)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    distribution_sample_order_id = fields.Many2one('distribution.sample.order', string='Distribution Sample Order')
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead')

    @api.model
    def create(self, vals):
        res = super(DistributeSampleProducts, self).create(vals)
        if res.distribution_sample_order_id:
            res.item_no = res.distribution_sample_order_id.distribution_sample_product_ids[-1].item_no + 1
        return res