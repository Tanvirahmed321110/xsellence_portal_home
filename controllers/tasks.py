from odoo import http
from odoo.http import request
from datetime import date
from odoo.tools import html2plaintext


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

        statuses = request.env['project.task'].sudo()._fields['custom_status'].selection

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
        status_selection = request.env['project.task'].sudo()._fields['custom_status'].selection

        # log message
        messages = request.env['mail.message'].sudo().search([
            ('model', '=', 'project.task'),
            ('res_id', '=', task.id),
            ('tracking_value_ids', '!=', False),
        ], order='date desc')

        return request.render('xsellence_portal.task_details_page', {
            'active_menu': 'tasks',
            'task': task,
            'status_selection': status_selection,
            'messages':messages,
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
        selected_project_id = kw.get('project_id')

        if source == 'tasks':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Add Task', 'url': False},
            ]
        elif source == 'projects':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Add Task', 'url': False},
            ]
        else:
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Add Task', 'url': False},
            ]

        projects = request.env['project.project'].sudo().search([])
        users = request.env['res.users'].sudo().search([])
        statuses = request.env['project.task'].sudo()._fields['custom_status'].selection
        priority = request.env['project.task'].sudo()._fields['custom_priority'].selection

        return request.render('xsellence_portal.add_task_page', {
            'active_menu': 'add_task',
            'breadcrumb': breadcrumb_data,
            'source': source,
            'projects': projects,
            'users': users,
            'statuses': statuses,
            'priority': priority,
            'today': date.today().strftime('%Y-%m-%d'),
            'selected_project_id': int(selected_project_id) if selected_project_id else False,
        })

    # ============  For Add Task Submit Page  ===============
    @http.route('/add_task/submit', tpe='http', auth='user', methods=['POST'], website=True, csrf=True)
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

        new_task = request.env['project.task'].sudo().create(task)

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

    # ==========================
    # POST - Edit Page Form Page
    # ==========================
    @http.route('/task/edit/<int:task_id>', type='http', auth='user', website=True, methods=['GET'], csrf=True)
    def edit_task_form(self, task_id, **kw):
        task = request.env['project.task'].sudo().browse(task_id)

        if not task.exists():
            return request.redirect('/tasks')

        projects = request.env['project.project'].sudo().search([])
        users = request.env['res.users'].sudo().search([])

        statuses = request.env['project.task'].sudo()._fields['custom_status'].selection
        priority = request.env['project.task'].sudo()._fields['custom_priority'].selection

        return request.render('xsellence_portal.edit_task_page', {
            'active_menu': 'tasks',
            'task': task,
            'task_description': html2plaintext(task.description or ''),
            'projects': projects,
            'users': users,
            'statuses': statuses,
            'priority': priority,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Edit Task', 'url': False},
            ]
        })

    # ========================
    # POST - Edit Task Submit
    # ========================
    @http.route('/task/edit/<int:task_id>', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def edit_task_submit(self, task_id, **kw):
        task = request.env['project.task'].sudo().browse(task_id)

        if not task.exists():
            return request.redirect('/tasks')

        assign_ids = request.httprequest.form.getlist('user_ids')
        user_ids = [(6, 0, [int(uid) for uid in assign_ids if uid])]

        vals = {
            'name': kw.get('name', task.name),
            'project_id': int(kw['project_id']) if kw.get('project_id') else False,
            'date_deadline': kw.get('date_deadline') or False,
            'custom_status': kw.get('custom_status', ''),
            'custom_priority': kw.get('custom_priority', ''),
            'description': kw.get('description', ''),
            'user_ids': user_ids,
        }

        task.write(vals)
        return request.redirect(f"/tasks/task_details/{task_id}")

    # =============  For Delete Task  ===============
    @http.route('/task/delete', type='http', auth='user', methods=['POST'], website=True)
    def delete_task(self, task_id=None, **kw):

        if not task_id:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Invalid Request',
                'error_desc': 'Task ID missing or invalid.',
                'error_btn_label': 'Show Tasks',
                'error_btn_url': '/tasks',
            })

        task = request.env['project.task'].sudo().browse(int(task_id))

        timesheets = request.env['account.analytic.line'].sudo().search([
            ('task_id', '=', task.id)
        ], limit=1)

        if timesheets:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Task Cannot Be Deleted',
                'error_desc': 'This task has timesheet entries. Please remove the timesheet entries first, then delete the task.',
                'error_btn_label': 'Back to Task',
                'error_btn_url': f'/tasks',
            })

        if task.exists():
            task.unlink()

        # ✅ Success Page
        return request.render('xsellence_portal.success_page', {
            'success_title': 'Task Successfully Deleted',
            'success_desc': 'Your task has been deleted successfully.',
            'success_btn_label': 'Show Tasks',
            'success_btn_url': '/tasks',
        })
