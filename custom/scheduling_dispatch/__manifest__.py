{
    'name': 'Scheduling & Dispatch App',
    'version': '1.0',
    'author': 'Hawkeye core',
    'category': 'Custom',
    'summary': 'Manage jobs and employee tasks',
    'description': 'Module to manage Scheduling & Dispatch App with views and portal integration.',
    'depends': ['base','base_setup'],
    'data': [
            'security/groups.xml',
            'security/ir.model.access.csv',
            'security/ir.rule.xml',
            'views/job_request_views.xml',
            'views/setting_inherit.xml',
            'views/project_monitor_views.xml',
            #'views/res_users_views.xml',
            #'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'scheduling_dispatch/static/src/js_inherit.xml',
        ],

    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}