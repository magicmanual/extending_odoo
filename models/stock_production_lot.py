from odoo import fields, models


class ProductionLot (models.Model):
    _inherit = 'stock.production.lot'
    expire_date=fields.Date(string='Expire Date',required=True)






