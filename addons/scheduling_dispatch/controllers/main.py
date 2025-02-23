from odoo import http
from odoo.http import request

class ProjectMonitorController(http.Controller):

    @http.route('/project_monitor_chart_data', type='json', auth='user')
    def get_chart_data(self):
        projects = request.env['project.monitor'].search([])
        data = [{
            'name': project.project_name,
            'overdue_jobs': project.overdue_jobs,
            'next_7_days_jobs': project.next_7_days_jobs,
            'after_7_days_jobs': project.after_7_days_jobs
        } for project in projects]
        return data