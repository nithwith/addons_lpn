# -*- coding: utf-8 -*-
{
    'name': "Event stage color",
    'version': '12.0.1.0.0',
    'summary': """Change color of calendar event with this stage""",
    'description': """This Module change color of calendar event with this stage""",
    'author': "Theo MARTY",
    'website': "https://github.com/nithwith",
    'category': 'Technical',
    'depends': ['base',
                'calendar',
                # 'web_widget_color'
                ],
    'data': [
        'views/template.xml',
        'views/event_views.xml',
        'security/ir.model.access.csv',
        'security/calendar_security.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
