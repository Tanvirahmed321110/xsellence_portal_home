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
    ], string=' Priority',default='normal', tracking=True)

    custom_status = fields.Selection([
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('review', 'Under Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Project Status', default='planning', tracking=True)

    # assign members
    assigned_user_ids = fields.Many2many(
        'res.users',
        string='Assigned Users',
        tracking=True
    )

    description = fields.Html(
        string='Description',
        tracking=True,
    )

    def _create_assignment_notifications(self, user_ids):
        Notification = self.env['xsellence.assignment.notification'].sudo()

        for task in self:
            for user_id in user_ids:
                Notification.create({
                    'user_id': user_id,
                    'title': 'Task Assigned',
                    'description': 'You have been added to %s task.' % task.name,
                    'view_url': '/tasks/task_details/%s' % task.id,
                    'res_model': 'project.task',
                    'res_id': task.id,
                })

    def _create_status_change_notifications(self, user_ids):
        Notification = self.env['xsellence.assignment.notification'].sudo()
        status_labels = dict(self._fields['custom_status'].selection)

        for task in self:
            status_label = status_labels.get(task.custom_status, task.custom_status)
            for user_id in user_ids:
                # Keep task status-change notifications in the same stream so
                # sidebar ordering and unread logic stay consistent.
                Notification.create({
                    'user_id': user_id,
                    'title': 'Task Status Changed',
                    'description': '%s task status changed to %s.' % (task.name, status_label),
                    'view_url': '/tasks/task_details/%s' % task.id,
                    'res_model': 'project.task',
                    'res_id': task.id,
                })

    @api.model_create_multi
    def create(self, vals_list):
        tasks = super().create(vals_list)

        for task in tasks:
            assigned_user_ids = set(task.user_ids.ids + task.assigned_user_ids.ids)

            if assigned_user_ids:
                task._create_assignment_notifications(assigned_user_ids)

        return tasks

    def write(self, vals):
        old_user_map = {
            task.id: set(task.user_ids.ids + task.assigned_user_ids.ids)
            for task in self
        }
        old_status_map = {
            task.id: task.custom_status
            for task in self
        }

        result = super().write(vals)

        if 'user_ids' in vals or 'assigned_user_ids' in vals:
            for task in self:
                new_user_ids = set(task.user_ids.ids + task.assigned_user_ids.ids)
                added_user_ids = new_user_ids - old_user_map.get(task.id, set())

                if added_user_ids:
                    task._create_assignment_notifications(added_user_ids)

        if 'custom_status' in vals:
            for task in self:
                if task.custom_status != old_status_map.get(task.id):
                    recipient_ids = set(task.user_ids.ids + task.assigned_user_ids.ids)
                    if recipient_ids:
                        task._create_status_change_notifications(recipient_ids)

        return result
