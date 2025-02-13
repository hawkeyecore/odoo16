from odoo import models, fields, api

class ProjectMonitor(models.Model):
    _name = 'project.monitor'
    _description = 'Project Monitor'

    name = fields.Char(string="Project Name")
    job_requests = fields.Many2many('job.request', string="Job Requests")
    assigned_user = fields.Many2one('res.users', string="Assigned User")
    assigned_customer_id = fields.Many2one('res.users', string='User', store=True, default=lambda self: self.env.user.id)


class ResUsers(models.Model):
    _inherit = "res.users"

    user_projects = fields.One2many(
        "project.monitor", "assigned_customer_id",
        string="Projects",
        domain="[('assigned_customer_id', '=', uid)]",  # Ensures only related records are shown
        readonly=True  # Makes it readonly
    )
