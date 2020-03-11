from odoo import models

class OutboundDelieveryOrder(models.Model):
    _name = 'report.outbound.delivery.order'
    _inherit = ['report.report_xlsx.abstract','account.invoice.report']

    def ensure_one_for_list(self,list):
            if len(list)==1:
                    return
            else:
                    raise Exception('length of list is not 1',list)


    def print_lot_and_expire_date(self,stock_production_lot_recordset,sheet,row,column,format_general,format_date):
            stock_production_lot_recordset.ensure_one()
            sheet.write(row,column,stock_production_lot_recordset.name,format_general)
            sheet.write(row,column+1, stock_production_lot_recordset.expire_date, format_date)
            return

    def write_one_row(self,sheet,row,single_record,format_general,format_date):
            column=0
            #write the first row
            sheet.write(row,column,'南宁',format_general)
            column+=1
            #print product_name,reference_code,manufacturer
            product_template=single_record.product_id
            sheet.write(row,column, product_template.name, format_general)
            column += 1
            sheet.write(row,column, product_template.default_code, format_general)
            column += 1
            sheet.write(row,column, product_template.manufacturer.name, format_general)
            column += 1

            # fetch lot_name and expire_date
            self.env.cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id=%s",(single_record.id,))
            order_line_list=self.env.cr.fetchall() #fetchall return a list of tuples
            self.ensure_one_for_list(order_line_list)
            order_line_id=order_line_list[0][0]
            sale_order_line= self.env['sale.order.line'].search([('id', '=', order_line_id)])
            stock_move=sale_order_line.move_ids
            stock_production_lot=stock_move.mapped('move_line_ids').mapped('lot_id')
            self.print_lot_and_expire_date(stock_production_lot,sheet,row,column,format_general,format_date)
            column+=2

            #print UOM
            uom_uom=single_record.product_uom_id
            sheet.write(row,column,uom_uom.name,format_general)
            column+=1

            #print quantity of the product
            sheet.write(row,column,single_record.quantity,format_general)
            column += 1

            #print price_average and price_subtotal
            sheet.write(row,column, single_record.price_average, format_general)
            column += 1
            sheet.write(row,column, single_record.price_subtotal, format_general)
            column += 1

            #print 供货单位许可证号
            sheet.write(row,column, '桂南食药监械经营许20170354号', format_general)
            column += 1
            #生产企业许可证号 单元格 画格子
            sheet.write(row,column, '', format_general)
            column += 1
            #print 注册证号

            column += 1
            #print 储运条件
            sheet.write(row,column, '常温', format_general)
            return







    def generate_xlsx_report(self, workbook, data, lines):

            sheet = workbook.add_worksheet()

            format_of_title=workbook.add_format({'font_size':14,'align':'center','bold':True})
            format_of_address= workbook.add_format({'font_size': 10, 'align': 'left'})
            format_of_table_head = workbook.add_format({'font_size': 9, 'align': 'center','valign':'vcenter','border':True,'text_wrap':True,'bold':True})
            format_of_table_content = workbook.add_format({'font_size': 9, 'align': 'center','valign':'vcenter','border':True,'text_wrap':True})
            format_of_table_content_date = workbook.add_format({'font_size': 9, 'align': 'center', 'valign': 'vcenter', 'border': True, 'text_wrap': True,'num_format':'yyyy-mm-dd'})

            sheet.merge_range('A1:N1','广西星远澜贸易有限公司销售出库单',format_of_title)
            sheet.merge_range('A2:N2','收货单位：国药控股广西有限公司',format_of_address)
            sheet.merge_range('A3:N3','=CONCATENATE("收货地址：广西南宁市江南区国凯大道东18号                          发货日期：",TEXT(TODAY(), "yyyy年mm月dd日"))',format_of_address)

            sheet.write('A4','仓库',format_of_table_head)
            sheet.write('B4', '商品名称', format_of_table_head)
            sheet.write('C4', '型号规格', format_of_table_head)
            sheet.write('D4', '生产厂家', format_of_table_head)
            sheet.write('E4', '批号', format_of_table_head)
            sheet.write('F4', '有效期', format_of_table_head)
            sheet.write('G4', '单位', format_of_table_head)
            sheet.write('H4', '数量', format_of_table_head)
            sheet.write('I4', '单价', format_of_table_head)
            sheet.write('J4', '金额', format_of_table_head)
            sheet.write('K4', '供货单位许可证号', format_of_table_head)
            sheet.write('L4', '生产企业许可证号', format_of_table_head)
            sheet.write('M4', '注册证号', format_of_table_head)
            sheet.write('N4', '储运条件', format_of_table_head)

            sheet.set_row(3,34)

            #single_record = self.browse(1)
            #self.write_one_row(sheet,4,single_record,format_of_table_content,format_of_table_content_date)
            row=4
            recordset = self.env['report.outbound.delivery.order'].search([])
            for record in recordset:
                    self.write_one_row(sheet,row,record,format_of_table_content,format_of_table_content_date)
                    row+=1



"""
            #write the first row
            sheet.write('A5','南宁',format_of_table_content)

            single_record=self.browse(1)
            #fetch product_name,reference_code,manufacturer
            product_template=single_record.product_id
            sheet.write('B5', product_template.name, format_of_table_content)
            sheet.write('C5', product_template.default_code, format_of_table_content)
            sheet.write('D5', product_template.manufacturer.name, format_of_table_content)

            #fetch lot_name and expire_date

            #sale_order_line_invoice_rel=self.env['sale.order.line.invoice.rel'].search([('id','in',single_record.id)])
            #sheet.write('E5', lines.sale_line_ids.id, format_of_table_content)

            self.env.cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id=%s",(single_record.id,))
            order_line_id=self.env.cr.fetchall()[0][0]  #fetchall return a list of tuples
            sale_order_line= self.env['sale.order.line'].search([('id', '=', order_line_id)])
            stock_move=sale_order_line.move_ids
            stock_production_lot=stock_move.mapped('move_line_ids').mapped('lot_id')
            self.print_lot_and_expire_date(stock_production_lot,sheet,4,4,format_of_table_content,format_of_table_content_date)

            #print UOM
            uom_uom=single_record.product_uom_id
            sheet.write('G5',uom_uom.name,format_of_table_content)

            #print quantity of the product
            sheet.write('H5',single_record.quantity,format_of_table_content)

            #print price_average and price_subtotal
            sheet.write('I5', single_record.price_average, format_of_table_content)
            sheet.write('J5', single_record.price_subtotal, format_of_table_content)

            #print 供货单位许可证号
            sheet.write('K5', '桂南食药监械经营许20170354号', format_of_table_content)
            #print 储运条件
            sheet.write('N5', '常温', format_of_table_content)
            #生产企业许可证号 单元格 画格子
            sheet.write('L5', '', format_of_table_content)
"""









