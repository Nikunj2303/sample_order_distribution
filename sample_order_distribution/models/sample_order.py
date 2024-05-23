from odoo import models, fields, api

class DistributionSampleOrder(models.Model):
    _name = 'distribution.sample.order'
    _description = 'Distribution Sample Order'

    name = fields.Char(string='Name', required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    source_location_id = fields.Many2one('stock.location', string='Source Location', required=True)
    destination_location_id = fields.Many2one('stock.location', string='Destination Location', required=True)
    user_id = fields.Many2one('res.users', string='Assigned to')
    distribution_sample_product_ids = fields.One2many('distribute.sample.products', 'distribution_sample_order_id',
                                                      string='Sample Products')

    @api.model
    def default_get(self, fields_list):
        res = super(DistributionSampleOrder, self).default_get(fields_list)
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        if warehouse:
            res['warehouse_id'] = warehouse.id
            res['source_location_id'] = warehouse.lot_stock_id.id
        return res

    @api.onchange('warehouse_id')
    def _onchange_warehouse_id(self):
        if self.warehouse_id:
            self.source_location_id = self.warehouse_id.lot_stock_id

    @api.onchange('user_id')
    def _onchange_user_id(self):
        if self.user_id:
            sample_location = self.env['stock.location'].search([('user_id', '=', self.user_id.id)], limit=1)
            self.destination_location_id = sample_location.id if sample_location else False

    def action_create_picking(self):
        for order in self:
            picking_vals = {
                'location_id': order.source_location_id.id,
                'location_dest_id': order.destination_location_id.id,
                'move_lines': [(0, 0, {
                    'name': product.product_id.name,
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.quantity,
                    'product_uom': product.product_id.uom_id.id,
                }) for product in order.distribution_sample_product_ids],
            }
            picking = self.env['stock.picking'].create(picking_vals)
            picking.action_confirm()
            picking.action_assign()
            if picking.state == 'assigned':
                picking.action_done()

    def action_auto_create_picking(self):
        for order in self:
            # Add your logic to automatically create and validate picking
            # This can be similar to the logic you provided in your original code
            pass

class DistributeSampleProducts(models.Model):
    _name = 'distribute.sample.products'
    _description = 'Distribute Sample Products'

    item_no = fields.Integer(string='Item No', default=1)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    distribution_sample_order_id = fields.Many2one('distribution.sample.order', string='Distribution Sample Order')
    crm_lead_id = fields.Many2one('crm.lead', string='CRM Lead')
