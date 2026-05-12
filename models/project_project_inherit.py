from odoo import models, fields, api
from datetime import date

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _order = 'create_date desc'


    custom_priority = fields.Selection([
        ('normal','normal'),
        ('medium','medium'),
        ('high','high'),
        ('urgent','urgent'),
    ], string=' Priority',default='medium')

    custom_status = fields.Selection([
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Project Status', default='planning')

    # assign members
    assigned_user_ids = fields.Many2many(
        'res.users',
        string='Assigned Users'
    )

    # 🔥 Remaining Days Field
    remaining_days = fields.Integer(
        string='Remaining Days',
        compute='_compute_remaining_days',
        store=True,
        readonly=True,
    )

    @api.depends('date')
    def _compute_remaining_days(self):
        today = date.today()

        for rec in self:
            if rec.date:
                rec.remaining_days = (rec.date - today).days
            else:
                rec.remaining_days = 0