# -*- coding: utf-8 -*-
{
    'name': "Event pos quotation",
    'version': '12.0.1.0.0',
    'summary': """This Module add link between pos quotation and events""",
    'description': """This Module add link between pos quotation and events""",
    'author': "Theo MARTY",
    'company': 'Theo MARTY',
    'website': "https://www.theomarty.fr",
    'category': 'Technical',
    'depends': ['base', 'calendar', 'pos_quotation_order'],
    'data': [
        'views/event_views.xml',
        'security/ir.model.access.csv',
        'security/calendar_security.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
