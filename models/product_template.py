from odoo import fields, models, api


class ProductTemplate (models.Model):
    _inherit = 'product.template'

    manufacturer=fields.Many2one('res.partner',string='Manufacturer')
    #manufacturer=fields.Char('Manufacturer',required=True)
    certificate_id=fields.Many2one('certificate.number',string='Certificate Number')

    type = fields.Selection([
        ('product', 'Storable Product'),
        ('service', 'Service')], string='Product Type', default='product',required=False,
        help='A storable product is a product for which you manage stock. The Inventory app has to be installed.\n'
             'A consumable product is a product for which stock is not managed.\n'
             'A service is a non-material product you provide.')

    tracking=fields.Selection([
        ('serial','By Unique Serial Number'),
        ('lot', 'By Lots')
    ],string='Tracking',default='lot',required=True
    )

    def _get_default_uom_id(self):
        return self.env["uom.uom"].search([('id','=',21)], limit=1, order='id').id

    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=True,
        help="Default unit of measure used for all stock operations.")


'''
    default_code = fields.Char(
        'Internal Reference', compute='_compute_default_code',
        inverse='_set_default_code', store=True,required=True)

    categ_id = fields.Many2one(
        'product.category', 'Product Category',
        change_default=True, default=_get_default_category_id, group_expand='_read_group_categ_id',
        required=False, help="Select category for the current product")

    uom_id = fields.Many2one(
        'uom.uom', 'Unit of Measure',
        default=_get_default_uom_id, required=False,
        help="Default unit of measure used for all stock operations.")

    uom_po_id = fields.Many2one(
        'uom.uom', 'Purchase Unit of Measure',
        default=_get_default_uom_id, required=False,
        help="Default unit of measure used for purchase orders. It must be in the same category as the default unit of measure.")
'''
    


