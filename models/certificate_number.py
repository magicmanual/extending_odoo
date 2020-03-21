from odoo import fields, models, api


class ModelName (models.Model):
    _name = 'certificate.number'
    _description = 'Certificate Number'

    name = fields.Char(string='Certificate Number')
    #manufacturer=fields.Char(String='Manufacturer')
    product_name=fields.Char(string='Product Name')
    is_imported=fields.Boolean('Is Imported',default=True)
    production_license=fields.Char(string='生产企业许可证号')
    #product_id=fields.One2many('product.template',string='product name2')
    


