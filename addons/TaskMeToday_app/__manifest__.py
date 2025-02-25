{
    'name': 'TaskMeToday App',
    'version': '1.0',
    'author': 'Hawkeye core',
    'category': 'Custom',
    'summary': 'Manage jobs and employee tasks',
    'description': 'Module to manage TaskMeToday App with views and portal integration.',
    'depends': ['base','base_setup','web'],
    'data': [
            'security/groups.xml',
            'security/ir.model.access.csv',
            'security/ir.rule.xml',
            'views/job_request_views.xml',
            'views/setting_inherit.xml',
            'views/project_monitor_views.xml',
            'views/hide_apps_menu.xml',
            'views/hide_odoo_logo.xml',
            'views/show_custom_app.xml',
            #'views/res_users_views.xml',
            #'views/menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'taskmetoday_app/static/src/js_inherit.xml',
            'taskmetoday_app/static/src/js/favicon.js',
            '/taskmetoday_app/static/src/css/project_monitor.css',
            #'/taskmetoday_app/static/src/js/project_monitor_chart.js',
        ],

    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}