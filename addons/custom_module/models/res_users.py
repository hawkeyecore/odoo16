from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    custom_group_ids = fields.Many2many(
        'res.groups',
        string='Custom Groups',
        help='Additional custom access rights for the user.'
    )
