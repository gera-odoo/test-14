# -*- coding: utf-8 -*-
{
    'name': "Nutrimental Info",

    'summary': """
        Nutrimental info label""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Gerardo Rafael Soto Maldonado",
    'license': 'OPL-1',
    'website': "https://www.linkedin.com/in/gerardosotomaldonado/",
    'support': 'gerasoma@gmail.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/products.xml',
        'views/fillers.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
