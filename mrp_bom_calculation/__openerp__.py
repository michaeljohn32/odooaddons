# -*- coding: utf-8 -*-
{
    'name': "mrp_bom_calculation",

    'summary': """
        This module calculates the unit_price of BoMs as they are produced
        """,

    'description': """
        This module calculates the unit_price of BoMs as they are produced
    """,

    'author': "John Walsh",
    'website': "http://github.com/michaeljohn32",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail', 'mrp', 'stock_account', 'stock','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
