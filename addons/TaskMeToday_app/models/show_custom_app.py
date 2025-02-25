from odoo import models, fields, api

class ModuleModule(models.Model):
    _inherit = "ir.module.module"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False):
        """ Modify the search to filter out marketplace apps. """
        domain.append(("author", "=", "TaskMeToday App"))  # Change 'Your Company' to match your custom apps' author
        return super(ModuleModule, self)._search(domain, offset, limit, order, count)