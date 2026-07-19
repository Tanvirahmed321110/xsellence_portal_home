from odoo import fields, models


class XsellenceAssignmentNotification(models.Model):
    _name = 'xsellence.assignment.notification'
    _description = 'Assignment Notification'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', required=True, index=True, ondelete='cascade')
    title = fields.Char(required=True)
    description = fields.Text(required=True)
    view_url = fields.Char(required=True)
    res_model = fields.Char(required=True, index=True)
    res_id = fields.Integer(required=True, index=True)
    is_read = fields.Boolean(default=False, index=True)
