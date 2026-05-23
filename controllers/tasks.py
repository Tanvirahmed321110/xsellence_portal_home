from odoo import http
from odoo.http import request
from datetime import date


class XsellencePortal(http.Controller):
    # =============  For Tasks Page  ===============
    @http.route('/tasks', type='http', auth='public', website=True)
    def tasks_f(self, project_id=None, **kw):

        domain = []

        user = request.env.user
        status = kw.get('status')

        # 🔥 Admin / Internal check
        if user.has_group('base.group_system'):
            # Admin → all tasks
            domain = []
        else:
            # portal user only assigned tasks
            domain = [('user_ids', 'in', [user.id])]

        if project_id:
            domain.append(('project_id', '=', int(project_id)))

        # 🔥 status filter
        if status:
            domain.append(('custom_status', '=', status))

        tasks = request.env['project.task'].sudo().search(domain)

        statuses = request.env['project.task'].fields_get(['custom_status'])['custom_status']['selection']

        return request.render('xsellence_portal.tasks_page', {
            'active_menu': 'tasks',
            'tasks': tasks,
            'statuses': statuses,
            'selected_status': status,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': False},
            ]
        })

    # =============  For Task Details Page  ===============
    @http.route('/tasks/task_details/<int:project_id>', type='http', auth='public', website=True)
    def task_details_f(self, project_id, **kw):

        task = request.env['project.task'].sudo().browse(project_id)
        status_selection = request.env['project.task'].fields_get(
            ['custom_status'])['custom_status']['selection']

        return request.render('xsellence_portal.task_details_page', {
            'active_menu': 'tasks',
            'task': task,
            'status_selection': status_selection,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Task Details', 'url': False},
            ]
        })

    # =================  For Task Update Status   ===================
    @http.route('/task/update_status', type='http', auth='user', methods=['POST'], csrf=True)
    def update_project_status(self, task_id=None, status=None, redirect_url=None, **kw):
        if task_id and status:
            task = request.env['project.task'].sudo().browse(int(task_id))
            task.write({'custom_status': status})

        if not redirect_url:
            return request.redirect(f"/tasks/task_details/{task_id}")
        return request.redirect(f"/tasks")

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
            'projects': projects,
            'users': users,
            'statuses': statuses,
            'priority': priority,
        })

    # ============  For Add Task Submit Page  ===============
    @http.route('/add_task/submit', tpe='http', auth='user', methods=['POST'], csrf=True)
    def add_task_submit(self, **kw):

        # Assignees (multiple select)
        assignee_ids = request.httprequest.form.getlist('user_ids')
        user_ids = [(6, 0, [int(uid) for uid in assignee_ids if uid])]

        task = {
            'name': kw.get('name'),
            'project_id': int(kw.get('project_id')) if kw.get('project_id') else False,
            'date_assign': kw.get('date_assign') or date.today(),
            'date_deadline': kw.get('date_deadline'),
            'custom_priority': kw.get('custom_priority'),
            'custom_status': kw.get('custom_status'),
            'user_ids': user_ids,
            'description': kw.get('description'),
        }

        new_task = request.env['project.task'].create(task)

        # ❌  Error Page
        if not new_task:
            return request.render('xsellence_portal.error_page', {
                'error_title': '❌ Task Creation Failed',
                'error_desc': 'Unable to create task.',
                'error_btn_label': 'Again Try',
                'error_btn_url': '/add_task',
            })
        # ✅ Success Page
        return request.render('xsellence_portal.success_page', {
            'success_title': 'Task Successfully Created',
            'success_desc': 'Your task has been added. You can now track it from the tasks list.',
            'success_btn_label': 'Show Tasks',
            'success_btn_url': '/tasks',
        })

    # =============  For Delete Task  ===============
    @http.route('/task/delete/<int:task_id>', type='http', auth='user', website=True)
    def delete_task(self, task_id, **kw):

        task = request.env['project.task'].sudo().browse(task_id)

        if task.exists():
            task.unlink()

        # ✅ Success Page
        return request.render('xsellence_portal.success_page', {
            'success_title': 'Task Successfully Deleted',
            'success_desc': 'Your task has been deleted successfully.',
            'success_btn_label': 'Show Tasks',
            'success_btn_url': '/tasks',
        })
