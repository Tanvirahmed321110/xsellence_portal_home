from odoo import models, fields, api
from datetime import date

class ProjectProject(models.Model):
    _inherit = 'project.task'
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
