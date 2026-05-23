from odoo import http
from odoo.http import request
from datetime import date

class XsellencePortal(http.Controller):
    @http.route('/timesheets', type='http', auth='public', website=True)
    def timesheet_f(self, **kw):
        return request.render('xsellence_portal.timesheet_page', {
            'active_menu': 'timesheets',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': False},
            ]
        })

    # For Add Timesheet Page
    @http.route('/add_timesheet', type='http', auth='public', website=True)
    def add_timesheet_f(self, **kw):

        source = kw.get('source')
        today = date.today()
        print(source)

        if source == 'timesheets':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': '/timesheets'},
                {'name': 'Add Timesheet', 'url': False},
            ]

        else:
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': False},
            ]

        return request.render('xsellence_portal.add_timesheet_page', {
            'active_menu': 'add_timesheet',
            'breadcrumb': breadcrumb_data,
            'today':today
        })




    # =============  Timesheet From Tasks  =============
    @http.route('/tasks/add_timesheet', type='http', auth='public', website=True)
    def add_timesheet_from_task(self, **kw):
        task_id = int(kw.get('task_id', 0))
        project_id = int(kw.get('project_id', 0))

        selected_task = request.env['project.task'].sudo().browse(task_id)
        selected_project = request.env['project.project'].sudo().browse(project_id)

        projects = request.env['project.project'].sudo().search([])
        tasks = request.env['project.task'].sudo().search([])

        return request.render('xsellence_portal.add_timesheet_page', {
            'active_menu': 'add_timesheet',
            'selected_task': selected_task,
            'tasks':tasks,
            'projects' : projects,
            'today': date.today(),
            'selected_project': selected_project,  # ✅ fixed
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Add Timesheet', 'url': False},
            ]
        })
