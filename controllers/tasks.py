from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):
    @http.route('/tasks', type='http', auth='public', website=True)
    def tasks_f(self, **kw):
        print('load dashboard')
        return request.render('xsellence_portal.tasks_page', {
            'active_menu': 'tasks',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': False},
            ]
        })

    # =============  For Task Details Page  ===============
    @http.route('/tasks/task_details', type='http', auth='public', website=True)
    def task_details_f(self, **kw):
        print('load dashboard')
        return request.render('xsellence_portal.task_details_page', {
            'active_menu': 'tasks',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Task Details', 'url': False},
            ]
        })



    # ============  For Add Task Page  ===============
    @http.route('/add_task', type='http', auth='public', website=True)
    def add_task_f(self, **kw):
        source = kw.get('source')

        if source == 'tasks':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Add Task', 'url': False},
            ]
        else:
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Add Task', 'url': False},
            ]

        return request.render('xsellence_portal.add_task_page', {
            'active_menu': 'add_task',
            'breadcrumb': breadcrumb_data,
            'source': source,
        })
