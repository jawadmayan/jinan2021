# -*- coding: utf-8 -*-
{
    'name': "Invoice Print",

    'summary': """
        
        """,

    'description': """
        
    """,

    'author': "Al Kidhma",
    'website': "http://www.alkidhma.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale','sale_margin','sale_enterprise'],
    'sequence' :1,
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/paper_format.xml',
        'views/views.xml',
        'views/external_layout_modify.xml',
        'views/print_wizard.xml',
        'views/sales_margin.xml',
        'views/Sale_report.xml',
        'views/templates.xml',
        'views/templates_ameera.xml',
        'views/company_inherit.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
