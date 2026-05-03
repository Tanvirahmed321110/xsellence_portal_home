from odoo import models, fields, api

class ProjectProject(models.Model):
    _inherit = 'project.project'


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
