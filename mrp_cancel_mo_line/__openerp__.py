# -*- coding: utf-8 -*-
{
    'name': "mrp_cancel_mo_line",

    'summary': """
        Adds a button to cancel a manufacturing order line
        """,

    'description': """
        Adds a button to cancel a manufacturing order line
    """,

    'author': "John Walsh",
    'website': "http://gitlab.com/michaeljohn32",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '0.1',

    # any module necessary for this one to work correctly

    # adding mrp_send_to_production for the button states
    #  in the view.xml
    'depends': ['mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/cancel_move_view.xml',
        'view/mrp_cancel_mo_line.xml',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
