from odoo import fields, models, api


class saleOrderLine (models.Model):
    _inherit = 'sale.order.line'

    is_mask_product=fields.Boolean('Is Mask Product',default=False)




