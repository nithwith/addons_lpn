# -*- coding: utf-8 -*-
{
    'name': "Custom POS Keyboard Shortcut",
    'summary': """
        Customized Point of Sale layout and keyboard shortcuts for desktop users
    """,
    'description': """
        Customized Point of Sale layout and keyboard shortcuts for desktop users
    """,
    'author': "Abdullah Al Arafat Bipul",
    'website': "http://www.scorpion9.com",
    'license': "LGPL-3",
    'support': "imbipul9@gmail.com",
    'category': 'point of sale',
    'version': '0.1',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': ['static/description/thumbnail.png'],
    'installable': True,
    'auto_install': False,
}