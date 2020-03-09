from odoo import fields, models, api


class SaleOrder (models.Model):
    _inherit = 'sale.order'

    patient_name=fields.Char(string='Patient Name')
    date_of_surgery=fields.Date(string='Date of surgery')
    department_of_surgery=fields.Char(string='Department of surgery')
    #department_of_surgery = fields.Char(string='手术科室')
    bed_coding=fields.Char(string='Bed Coding')
    surgeon=fields.Char(string='Surgeon')
    operating_nurse=fields.Char(string='Operating nurse')


