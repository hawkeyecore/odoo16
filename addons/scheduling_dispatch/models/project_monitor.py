from odoo import models, fields, api
from datetime import timedelta

class ProjectMonitor(models.Model):
    _name = 'project.monitor'
    _description = 'Project Monitor'

    name = fields.Char(string="Project Name")
    job_requests = fields.Many2many('job.request', string="Job Requests")

    total_jobs = fields.Integer(string="Total Jobs", compute="_compute_job_counts", store=True)
    next_7_days = fields.Integer(string="Next 7 Days Jobs", compute="_compute_job_counts", store=True)
    after_7_days = fields.Integer(string="After 7 Days Jobs", compute="_compute_job_counts", store=True)
    overdue_jobs = fields.Integer(string="Overdue Jobs", compute="_compute_job_counts", store=True)

    @api.depends('job_requests', 'job_requests.start_date', 'job_requests.create_date')
    def _compute_job_counts(self):
        for record in self:
            total = len(record.job_requests)
            next_7_days_count = 0
            after_7_days_count = 0
            overdue_count = 0

            for job in record.job_requests:
                if job.start_date and job.create_date:
                    start_date = job.start_date.date()   # Likely a Date field
                    create_date = job.create_date.date()  # Convert Datetime to Date

                    days_difference = (start_date - create_date).days  # Calculate day difference

                    if days_difference < 0:
                        overdue_count += 1  # Overdue Jobs
                    elif 0 <= days_difference <= 7:
                        next_7_days_count += 1  # Next 7 Days Jobs
                    else:
                        after_7_days_count += 1  # After 7 Days Jobs

            record.total_jobs = total
            record.next_7_days = next_7_days_count
            record.after_7_days = after_7_days_count
            record.overdue_jobs = overdue_count

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
