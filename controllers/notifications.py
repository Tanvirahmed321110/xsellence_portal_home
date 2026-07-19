from odoo import http
from odoo.http import request


class XsellencePortalNotifications(http.Controller):

    @http.route('/assignment/notifications', type='json', auth='user', website=True)
    def assignment_notifications(self, **kw):
        notifications = request.env['xsellence.assignment.notification'].sudo().search([
            ('user_id', '=', request.env.user.id),
            ('is_read', '=', False),
        ], order='create_date desc', limit=10)

        return [{
            'id': notification.id,
            'title': notification.title,
            'desc': notification.description,
            'view_url': notification.view_url,
        } for notification in notifications]

    @http.route('/assignment/notifications/read', type='json', auth='user', website=True)
    def assignment_notification_read(self, notification_id=None, **kw):
        if notification_id:
            notification = request.env['xsellence.assignment.notification'].sudo().search([
                ('id', '=', int(notification_id)),
                ('user_id', '=', request.env.user.id),
            ], limit=1)

            if notification:
                notification.write({'is_read': True})

        return {'success': True}
