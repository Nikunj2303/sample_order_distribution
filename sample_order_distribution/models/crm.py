from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    distribution_sample_product_ids = fields.One2many('distribute.sample.products', 'crm_lead_id', string='Sample Products')

    def action_create_picking(self):
        for lead in self:
            picking_vals = {
                'location_id': self.env.user.context_default_warehouse_id.lot_stock_id.id,
                'location_dest_id': lead.partner_id.property_stock_customer.id,
                'move_lines': [(0, 0, {
                    'name': product.product_id.name,
                    'product_id': product.product_id.id,
                    'product_uom_qty': product.quantity,
                    'product_uom': product.product_id.uom_id.id,
                }) for product in lead.distribution_sample_product_ids],
            }
            picking = self.env['stock.picking'].create(picking_vals)
            picking.action_confirm()
            picking.action_assign()
            if picking.state == 'assigned':
                picking.action_done()
