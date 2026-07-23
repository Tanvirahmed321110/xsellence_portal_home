from odoo import models, fields, api
from datetime import date

class ProjectProject(models.Model):
    _inherit = 'project.project'
    _order = 'create_date desc'

    # For Useful link links page
    github_link = fields.Char(string='Github Repo Link',tracking=True)
    live_link  = fields.Char(string='Live Link',tracking=True)
    live_user  = fields.Char(string='Live User',tracking=True)
    live_password  = fields.Char(string='Live Password',tracking=True)

    dev_link = fields.Char(string='Dev Server Link',tracking=True)
    dev_user = fields.Char(string='Dev Server User',tracking=True)
    dev_password = fields.Char(string='Dev Server Password',tracking=True)

    assigned_user_ids = fields.Many2many(
        'res.users',
        tracking=True,
    )

    user_id = fields.Many2one(
        'res.users',
        tracking=True,
    )


    custom_priority = fields.Selection([
        ('normal','normal'),
        ('medium','medium'),
        ('high','high'),
        ('urgent','urgent'),
    ], string=' Priority',default='normal')

    custom_status = fields.Selection([
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Project Status', default='planning',tracking=True)

    # assign members
    assigned_user_ids = fields.Many2many(
        'res.users',
        string='Assigned Users',
        tracking=True
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

    allocated_hours = fields.Float(
        compute="_compute_allocated_hours",
        store=True,
        readonly=False
    )

    @api.depends("date_start", "date")
    def _compute_allocated_hours(self):
        for rec in self:
            if rec.date_start and rec.date:
                delta = rec.date - rec.date_start
                rec.allocated_hours = delta.days * 8
            else:
                rec.allocated_hours = 0.0

    def _create_assignment_notifications(self, user_ids):
        Notification = self.env['xsellence.assignment.notification'].sudo()

        for project in self:
            for user_id in user_ids:
                Notification.create({
                    'user_id': user_id,
                    'title': 'Project Assigned',
                    'description': 'You have been added to %s project.' % project.name,
                    'view_url': '/projects/details/%s' % project.id,
                    'res_model': 'project.project',
                    'res_id': project.id,
                })

    def _create_status_change_notifications(self, user_ids):
        Notification = self.env['xsellence.assignment.notification'].sudo()
        status_labels = dict(self._fields['custom_status'].selection)

        for project in self:
            status_label = status_labels.get(project.custom_status, project.custom_status)
            for user_id in user_ids:
                # Reuse the same notification model so popup and sidebar both
                # receive project status updates without any extra table.
                Notification.create({
                    'user_id': user_id,
                    'title': 'Project Status Changed',
                    'description': '%s project status changed to %s.' % (project.name, status_label),
                    'view_url': '/projects/details/%s' % project.id,
                    'res_model': 'project.project',
                    'res_id': project.id,
                })

    @api.model_create_multi
    def create(self, vals_list):
        projects = super().create(vals_list)

        for project in projects:
            assigned_user_ids = set(project.assigned_user_ids.ids)
            if project.user_id:
                assigned_user_ids.add(project.user_id.id)

            if assigned_user_ids:
                project._create_assignment_notifications(assigned_user_ids)

        return projects

    def write(self, vals):
        old_user_map = {
            project.id: set(project.assigned_user_ids.ids + project.user_id.ids)
            for project in self
        }
        old_status_map = {
            project.id: project.custom_status
            for project in self
        }

        result = super().write(vals)

        if 'assigned_user_ids' in vals or 'user_id' in vals:
            for project in self:
                new_user_ids = set(project.assigned_user_ids.ids + project.user_id.ids)
                added_user_ids = new_user_ids - old_user_map.get(project.id, set())

                if added_user_ids:
                    project._create_assignment_notifications(added_user_ids)

        if 'custom_status' in vals:
            for project in self:
                if project.custom_status != old_status_map.get(project.id):
                    recipient_ids = set(project.assigned_user_ids.ids + project.user_id.ids)
                    if recipient_ids:
                        project._create_status_change_notifications(recipient_ids)

        return result
