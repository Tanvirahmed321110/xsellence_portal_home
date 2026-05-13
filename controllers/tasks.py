from odoo import http
from odoo.http import request
from datetime import date


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

        projects = request.env['project.project'].search([])
        users = request.env['res.users'].search([])
        statuses = request.env['project.task']._fields['custom_status'].selection
        priority = request.env['project.task']._fields['custom_priority'].selection

        return request.render('xsellence_portal.add_task_page', {
            'active_menu': 'add_task',
            'breadcrumb': breadcrumb_data,
            'source': source,
            'projects':projects,
            'users':users,
            'statuses':statuses,
            'priority':priority,
        })



    # ============  For Add Task Submit Page  ===============
    @http.route('/add_task/submit',tpe='http',auth='user',methods=['POST'],csrf=True)
    def add_task_submit(self,**kw):

        # Assignees (multiple select)
        assignee_ids = request.httprequest.form.getlist('user_ids')
        user_ids = [(6, 0, [int(uid) for uid in assignee_ids if uid])]

        task = {
            'name':kw.get('name'),
            'project_id': int(kw.get('project_id')) if kw.get('project_id') else False,
            'date_assign': kw.get('date_assign') or date.today(),
            'date_deadline': kw.get('date_deadline'),
            'custom_priority': kw.get('custom_priority', '1'),
            'custom_status': kw.get('custom_status', '1'),
            'user_ids' : user_ids,
            'description':kw.get('description'),
        }

        request.env['project.task'].create(task)
        # ✅ Success Page
        return request.render('xsellence_portal.success_page',{
            'success_title': 'Task Successfully Created',
            'success_desc': 'Your task has been added. You can now track it from the tasks list.',
            'success_btn_label': 'Show Tasks',
            'success_btn_url': '/tasks',
        })