from odoo import models

class OutboundDelieveryOrder(models.AbstractModel):
    _name = 'report.extending_odoo.outbound_delivery_order'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

            sheet = workbook.add_worksheet()

            format1=workbook.add_format({'font_size':14,'align':'vcenter','bold':True})
            format2=workbook.add_format({'font_size':10,'align':'vcenter'})
            sheet.write(2,2,'Name',format1)
            sheet.write(2,3,lines.invoice_partner_display_name,format2)

