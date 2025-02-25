from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class JobRequest(models.Model):
    _name = 'job.request'
    _description = 'Job Request'

    #name = fields.Char(string='Job Title', required=True)
    name = fields.Selection([
    ('job1', 'Job-1'),
    ('job2', 'Job-2'),
    ('job3', 'Job-3'),
    ('job4', 'Job-4')
    ], string='Job Title', required=True)

    project_id = fields.Many2one('project.monitor', string="Project")
    description = fields.Text(string='Test() Description')
    # status = fields.Selection([
    #     ('new_job', 'New Job'),
    #     ('accept_job', 'Accept Job'),
    #     ('in_progress', 'In Progress'),
    #     ('rescheduled', 'Rescheduled'),
    #     ('completed', 'Completed'),
    #     ('close', 'Close'),
    # ], string='Status', default='new_job')
    status = fields.Selection(selection=lambda self: self._get_status_selection(),
                              string='Status', default='new_job')

    def _get_status_selection(self):
        # Base options for all users
        selections = [
            ('new_job', 'New Job'),
            ('accept_job', 'Accept Job'),
            ('in_progress', 'In Progress'),
            ('rescheduled', 'Rescheduled'),
            ('completed', 'Completed'),
        ]
        # Append 'close' option only if user is a manager
        if self.env.user.has_group('TaskMeToday_app.group_manager'):
            selections.append(('close', 'Close'))
        return selections

    can_edit_job_completed = fields.Boolean(
        string="Can Edit Job Completed",
        compute="_compute_can_edit_job_completed",
        store=True,
    )

    @api.depends('status')
    def _compute_can_edit_job_completed(self):
        for rec in self:
            rec.can_edit_job_completed = (rec.status == 'close')


    submitted_by = fields.Many2one(
    'res.users',
    string='Customer',
    default=lambda self: self.env.user
    )

    status_date = fields.Selection([
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('red', 'Red'),
    ], string='Status', compute='_compute_status', store=True)

    @api.depends('start_date', 'create_date')
    def _compute_status(self):
        for record in self:
            if not record.start_date or not record.create_date:
                record.status_date = False
                continue

            create_date = record.create_date.date()  # Convert Datetime to Date
            start_date = record.start_date.date()  # Already a Date field
            days_difference = (start_date - create_date).days  # Calculate difference in days

            if days_difference < 0:
                record.status_date = 'red'  # Start date is before creation → Overdue
            elif 0 <= days_difference <= 7:
                record.status_date = 'yellow'  # Start date is within 7 days of creation
            else:
                record.status_date = 'green'

    @api.model
    def create(self, vals):
        _logger.info(f"Creating Job Request: {vals}")
        job = super(JobRequest, self).create(vals)
        if job.project_id:
            job.project_id.write({'job_requests': [(4, job.id)]})  # Add job to the project's job_requests field
        return job


    assigned_user_id = fields.Many2one('res.users', string='Assigned User')
    #requested_by = fields.Many2one('res.users', string='Customer', default=lambda self: self.env.user.id)

    task_notes = fields.Text( string='Task Notes' )
    start_date = fields.Datetime(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date', required=True)
    color = fields.Integer(string='Color', compute='_compute_color', store=True)
    job_completed = fields.Datetime(
            string='Job Completed Date & Time',
            readonly=True,
            store=True,
            help="The date and time when the job was marked as completed."
        )
    # Automatically set job_completed when the status changes to 'completed'
    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'completed' and not self.job_completed:
            self.job_completed = fields.Datetime.now()    
    
    def write(self, vals):
        # Check if the status is being changed to 'completed'
        if 'status' in vals and vals['status'] == 'completed':
            for record in self:
                if not record.job_completed:
                    record.job_completed = fields.Datetime.now()

        for job in self:
            old_project = job.project_id  # Store old project before update
            old_status = job.status  # Store old status before update

            res = super(JobRequest, self).write(vals)
            new_project = self.project_id if 'project_id' in vals else old_project
            new_status = vals.get('status', old_status)  # Get new status if updated

            if old_project and old_project != new_project:
                old_project.write({'job_requests': [(3, job.id)]})  # Remove from old project

            if new_project and new_status != 'close':
                new_project.write({'job_requests': [(4, job.id)]})  # Add to new project

            # Remove from job_requests if status is changed to 'close'
            if new_status == 'close' and job.project_id:
                job.project_id.write({'job_requests': [(3, job.id)]})

        return res

    # Methods
    def action_accept_job(self):
        """Allow employees to accept jobs."""
        if self.env.user.id == self.assigned_user_id.id:
            self.status = 'in_progress'

    def action_reassign(self, new_employee_id):
        """Allow managers to reassign jobs."""
        if self.env.user.has_group('TaskMeToday_app.group_manager'):
            self.assigned_user_id = new_employee_id

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("The start date cannot be after the end date.")

    def action_complete_job(self):
        if self.env.user.has_group('TaskMeToday_app.group_manager'):
            self.status = 'completed'

    @api.depends('status')
    def _compute_color(self):
        for record in self:
            if record.status == 'new_job':
                record.color = 1  # Red
            elif record.status == 'in_progress':
                record.color = 2  # Blue
            elif record.status == 'rescheduled':
                record.color = 3  # Green
            elif record.status == 'completed':
                record.color = 4  # Purple

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=False,
        readonly=True
    )

    @api.depends('name', 'submitted_by', 'assigned_user_id')
    def _compute_display_name(self):
        for record in self:
            job_name = record.name or "Missing Job Title"
            customer_name = record.submitted_by.name if record.submitted_by else ""

            # Dynamically hide employee name for customers
            if self.env.user.has_group('TaskMeToday_app.group_customer'):
                employee_name = ""
            else:
                employee_name = record.assigned_user_id.name if record.assigned_user_id else ""

            record.display_name = f"{job_name} - {customer_name} - {employee_name}"