from odoo import models,api
from xlsxwriter.utility import xl_range
import cn2an
import re

class OutboundDelieveryOrder(models.Model):
    _name = 'report.outbound.delivery.order'
    _inherit = ['report.report_xlsx.abstract','account.invoice.report']

    def write_production_licence(self,product_template,sheet,row,column,format_general):
            if product_template.certificate_id.is_imported==True:
                    sheet.write(row, column, '', format_general)
            else:
                    sheet.write(row, column,product_template.certificate_id.production_license , format_general)
            return


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

    def write_table_header(self,sheet,format_of_title,format_of_address,format_of_table_head,):
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
            #sheet.write(row,column, '', format_general)
            self.write_production_licence(product_template,sheet,row,column,format_general)
            column += 1
            #print 注册证号
            sheet.write(row,column, product_template.certificate_id.name, format_general)

            column += 1
            #print 储运条件
            sheet.write(row,column, '常温', format_general)
            return







    def generate_xlsx_report(self, workbook, data, lines):





            format_of_title=workbook.add_format({'font_size':14,'align':'center','bold':True})
            format_of_address= workbook.add_format({'font_size': 10, 'align': 'left'})
            format_of_table_head = workbook.add_format({'font_size': 9, 'align': 'center','valign':'vcenter','border':True,'text_wrap':True,'bold':True})
            format_of_table_content = workbook.add_format({'font_size': 9, 'align': 'center','valign':'vcenter','border':True,'text_wrap':True})
            format_of_table_content_date = workbook.add_format({'font_size': 9, 'align': 'center', 'valign': 'vcenter', 'border': True, 'text_wrap': True,'num_format':'yyyy-mm-dd'})
            format_company_info=workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter'})
            format_of_table_content_address = workbook.add_format({'font_size': 9, 'align': 'left', 'valign': 'vcenter', 'border': True, 'text_wrap': True})


            #single_record = self.browse(1)
            #self.write_one_row(sheet,4,single_record,format_of_table_content,format_of_table_content_date)
            row=4
            #get current invoice id
            #invoice_id=self.invoice_ids.id

            invoice_id=int(re.findall('\d+',data['data'])[0])
            recordset = self.env['report.outbound.delivery.order'].search([('move_id','=',invoice_id)])

            single_record=recordset[0]
            self.env.cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id=%s",(single_record.id,))
            order_line_list=self.env.cr.fetchall() #fetchall return a list of tuples
            self.ensure_one_for_list(order_line_list)
            order_line_id=order_line_list[0][0]
            sale_order_line= self.env['sale.order.line'].search([('id', '=', order_line_id)])
            sale_order=sale_order_line.order_id

            account_move=self.env['account.move'].browse(invoice_id)

            sheet = workbook.add_worksheet((account_move.invoice_partner_display_name if account_move.invoice_partner_display_name != False else 'false')+' '+(sale_order.patient_name if sale_order.patient_name != False else 'false')+' '+(sale_order.date_of_surgery.strftime("%Y-%m-%d") if sale_order.date_of_surgery != False else 'false' ))

            #sheet = workbook.add_worksheet(account_move.invoice_partner_display_name+' '+sale_order.patient_name+' '+sale_order.date_of_surgery.strftime("%Y-%m-%d"))

            self.write_table_header(sheet,format_of_title,format_of_address,format_of_table_head)



            for record in recordset:
                    self.write_one_row(sheet,row,record,format_of_table_content,format_of_table_content_date)
                    row+=1
                    print('print out delivery for invoice_id=',invoice_id)
                    print('patient name is: ', sale_order.patient_name)
                    print((account_move.invoice_partner_display_name if account_move.invoice_partner_display_name != False else 'false'))


            #write the tail of table
            sheet.merge_range(row,0,row,4,'合计',format_of_table_content)
            sum_range= xl_range(4,9,row-1,9)
            sum_formula='=SUM(%s)' % sum_range
            sheet.merge_range(row, 5, row, 13,sum_formula , format_of_table_content)
            row+=1
            #write chinese total
            sheet.merge_range(row, 0, row, 1, '金额合计（大写）：', format_of_table_content)
            total_in_chinese=cn2an.an2cn(account_move.amount_total,"rmb")
            sheet.merge_range(row, 2, row, 13, total_in_chinese, format_of_table_head)
            row+=1
            #write info of our company
            sheet.merge_range(row, 0, row, 13, '公司地址：广西南宁市白沙大道35号南国花园商城D1栋D1-2号、D1-4号房', format_of_table_content_address)
            row+=1
            sheet.write(row, 0, '备注:', format_company_info)
            sheet.merge_range(row, 1, row, 13, '1、本发货单加盖本公司印章方可提货，提货前与仓库联系。', format_company_info)
            row+=1
            sheet.merge_range(row, 1, row, 13, '2、客户提货时请验看货物，出库后不接受无理由退货。', format_company_info)
            row+=1
            sheet.merge_range(row, 1, row, 13, '3、请客户在发货单有效期内提货，如逾期或未提货，须重新办理有关手续，由此产生的一切费用由需方自理。', format_company_info)
            row+=1
            sheet.merge_range(row, 1, row, 13, '4、此发货单一式五联，第一联：存根（白）第二联：结算（粉）第三联：保管（绿）第四联：装货（蓝）。', format_company_info)
            row+=1
            sheet.merge_range(row, 1, row, 13, '5、如有问题，请及时与本公司联系。', format_company_info)
            row+=1
            sheet.merge_range(row, 0, row, 13, '  制单：唐舒恩              提货人：彭军          客户签收：              签收日期：', format_company_info)






            return









