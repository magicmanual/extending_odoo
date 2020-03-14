from odoo import fields, models, api


class resPartner (models.Model):
    _inherit = 'res.partner'

    abbreviation= fields.Char('Abbreviation')
    


