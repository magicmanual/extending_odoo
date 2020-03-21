# -*- coding: utf-8 -*-
{
    'name': "extendingOdoo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Wu Hua",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock',
                'product',
                'sale',
                'crm',
                #copy
                'base_setup',
                'sales_team',
                'mail',
                'calendar',
                'resource',
                'fetchmail',
                'utm',
                'web_tour',
                'contacts',
                'digest',
                'phone_validation',
                'sale_stock',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_production_lot_tree_extending.xml',
        'views/stock_move_line_operations_tree_extending.xml',
        'views/product_template_product_form.xml',
        'views/stock_production_lot_form.xml',
        'reports/invoicing_outbound_delivery_order.xml',
        'views/sale_order_form_ext.xml',
        'security/ir.model.access.csv',
        'views/res_partner_form.xml',
        'views/sale_order_form_sale_stock_ext.xml',
        'views/sale_order_tree_ext.xml',

    ],

    'application': False,

}
