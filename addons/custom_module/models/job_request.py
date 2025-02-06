from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import logging
from datetime import datetime

_logger = logging.getLogger(__name__)

class JobRequest(models.Model):
    _name = 'job.request'
    _description = 'Job Request'

    name = fields.Char(string='Job Title', required=True)
    description = fields.Text(string='Test() Description')
    status = fields.Selection([
        ('new_job', 'New Job'),
        ('in_progress', 'In Progress'),
        ('rescheduled', 'Rescheduled'),
        ('completed', 'Completed'),
    ], string='Status', default='new_job')

    submitted_by = fields.Many2one(
    'res.users',
    string='Customer',
    default=lambda self: self.env.user
    )

    @api.model
    def create(self, vals):
        _logger.info(f"Creating Job Request: {vals}")
        return super(JobRequest, self).create(vals)

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
        return super(JobRequest, self).write(vals)

    # Methods
    def action_accept_job(self):
        """Allow employees to accept jobs."""
        if self.env.user.id == self.assigned_user_id.id:
            self.status = 'in_progress'

    def action_reassign(self, new_employee_id):
        """Allow managers to reassign jobs."""
        if self.env.user.has_group('custom_module.group_manager'):
            self.assigned_user_id = new_employee_id

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date > record.end_date:
                raise ValidationError("The start date cannot be after the end date.")

    def action_complete_job(self):
        if self.env.user.has_group('custom_module.group_manager'):
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
        store=True,
        readonly=True
    )

    @api.depends('name', 'submitted_by', 'assigned_user_id')
    def _compute_display_name(self):
        for record in self:
            job_name = record.name or "Missing Job Title"
            customer_name = (
                record.submitted_by.name
                if self.env.user.has_group('custom_module.group_manager')
                else "Restricted"
            )
            employee_name = (
                record.assigned_user_id.name
                if self.env.user.has_group('custom_module.group_manager')
                else "Restricted"
            )
            record.display_name = f"{job_name} - {customer_name} - {employee_name}"