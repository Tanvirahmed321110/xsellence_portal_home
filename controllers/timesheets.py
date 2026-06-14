import re
from odoo import http
from odoo.http import request
from datetime import date
from dateutil.relativedelta import relativedelta


class XsellencePortal(http.Controller):
    def _convert_time_input_to_float(self, time_value):
        """
        Input:
            1.7  = 1 hour 7 minutes
            1.22 = 1 hour 22 minutes
            1.30 = 1 hour 30 minutes
            2.45 = 2 hours 45 minutes

        Odoo saves:
            1.116667 = 1 hour 7 minutes
            1.366667 = 1 hour 22 minutes
            1.5      = 1 hour 30 minutes
            2.75     = 2 hours 45 minutes
        """

        time_value = str(time_value or "0").strip()

        # allow: 1, 1.7, 1.07, 1.22, 1.59
        if not re.match(r"^\d+(\.(\d|[0-5]\d))?$", time_value):
            raise ValueError("Invalid time format")

        if "." not in time_value:
            return float(time_value)

        hour_part, minute_part = time_value.split(".")

        hours = int(hour_part)
        minutes = int(minute_part)

        if minutes >= 60:
            raise ValueError("Minutes must be less than 60")

        return hours + (minutes / 60.0)



    # =============  Timesheet Page  =============
    @http.route('/timesheets', type='http', auth='user', website=True)
    def timesheet_f(self, **kw):
        user = request.env.user

        selected_month = kw.get('month', '')
        selected_project_id = int(kw.get('project_id') or 0)

        employees = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ])

        base_domain = [
            '|',
            ('user_id', '=', user.id),
            ('employee_id', 'in', employees.ids),
        ]

        # ==============================
        # Fast Project Dropdown using read_group
        # ==============================
        project_groups = request.env['account.analytic.line'].sudo().read_group(
            domain=base_domain + [('project_id', '!=', False)],
            fields=['project_id'],
            groupby=['project_id'],
            lazy=False,
        )

        project_ids = [
            group['project_id'][0]
            for group in project_groups
            if group.get('project_id')
        ]

        project_filter_options = request.env['project.project'].sudo().browse(project_ids).sorted(
            lambda p: p.name or ''
        )

        # ==============================
        # Last 12 months
        # ==============================
        today = date.today()
        current_month_start = today.replace(day=1)

        month_options = []
        for i in range(11, -1, -1):
            month_start = current_month_start - relativedelta(months=i)

            month_options.append({
                'value': month_start.strftime('%Y-%m'),
                'label': month_start.strftime('%b %Y'),
            })

        # ==============================
        # Final table domain
        # ==============================
        domain = list(base_domain)

        if selected_project_id:
            domain.append(('project_id', '=', selected_project_id))

        if selected_month:
            try:
                month_start = date.fromisoformat(selected_month + '-01')
                month_end = month_start + relativedelta(months=1)

                domain += [
                    ('date', '>=', month_start.strftime('%Y-%m-%d')),
                    ('date', '<', month_end.strftime('%Y-%m-%d')),
                ]
            except ValueError:
                selected_month = ''

        timesheets = request.env['account.analytic.line'].sudo().search(
            domain,
            order='date desc, id desc',
            limit=100
        )

        return request.render('xsellence_portal.timesheet_page', {
            'active_menu': 'timesheets',
            'timesheets': timesheets,

            'month_options': month_options,
            'selected_month': selected_month,

            'project_filter_options': project_filter_options,
            'selected_project_id': selected_project_id,

            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': False},
            ]
        })


    #==============  For Add Timesheet Page
    @http.route('/add_timesheet', type='http', auth='public', website=True)
    def add_timesheet_f(self, **kw):
        source = kw.get('source')
        today = date.today()

        projects = request.env['project.project'].sudo().search([])
        tasks = request.env['project.task'].sudo().search([])

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
            'today': today,
            'projects': projects,
            'tasks': tasks,
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
            'tasks': tasks,
            'projects': projects,
            'today': date.today(),
            'selected_project': selected_project,  # ✅ fixed
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Tasks', 'url': '/tasks'},
                {'name': 'Add Timesheet', 'url': False},
            ]
        })


    # =============  Timesheet From Submit  =============
    @http.route('/tasks/add_timesheet/submit', type='http', auth='user', website=True, methods=['POST'])
    def add_timesheet_from_submit(self, **kw):
        task_id = int(kw.get('task_id', 0))
        project_id = int(kw.get('project_id', 0))

        try:
            unit_amount = self._convert_time_input_to_float(kw.get('unit_amount'))
        except ValueError:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Invalid Time Spent',
                'error_desc': 'Please enter valid time. Example: 1.5 = 1 hour 30 minutes, 1.22 = 1 hour 22 minutes.',
                'error_btn_label': 'Go Back',
                'error_btn_url': f'/tasks/add_timesheet?task_id={task_id}&project_id={project_id}',
            })

        date_str = kw.get('date')
        description = kw.get('name', '')
        task_id = int(kw.get('task_id', 0))
        project_id = int(kw.get('project_id', 0))
        try:
            unit_amount = self._convert_time_input_to_float(kw.get('unit_amount'))
        except ValueError:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Invalid Time Spent',
                'error_desc': 'Please enter valid time. Example: 1.5 = 1 hour 30 minutes, 1.22 = 1 hour 22 minutes.',
                'error_btn_label': 'Go Back',
                'error_btn_url': f'/tasks/add_timesheet?task_id={task_id}&project_id={project_id}',
            })
        date_str = kw.get('date')
        description = kw.get('name', '')

        employee = request.env['hr.employee'].sudo().search(
            [('user_id', '=', request.env.user.id)], limit=1
        )

        # ❌ Employee
        if not employee:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Employee Not Found',
                'error_desc': 'No employee record linked to your account. Please contact admin.',
                'error_btn_label': 'Go Back',
                'error_btn_url': f'/tasks/add_timesheet?task_id={task_id}&project_id={project_id}',
            })

        vals = {
            'task_id': task_id,
            'project_id': project_id,
            'employee_id': employee.id,
            'date': date_str,
            'name': description,
            'unit_amount': unit_amount,
        }

        timesheet = request.env['account.analytic.line'].sudo().create(vals)

        # ❌ Error
        if not timesheet:
            return request.render('xsellence_portal.error_page', {
                'error_title': '❌ Timesheet Creation Failed',
                'error_desc': 'Unable to save timesheet entry.',
                'error_btn_label': 'Try Again',
                'error_btn_url': f'/tasks/add_timesheet?task_id={task_id}&project_id={project_id}',
            })

        # ✅ Success
        return request.render('xsellence_portal.success_page', {
            'success_title': '✔️ Timesheet Submitted',
            'success_desc': 'Your timesheet entry has been saved successfully.',
            'success_btn_label': 'View Timesheets',
            'success_btn_url': '/timesheets',
        })



    # =============  Delete Timesheet  =============
    @http.route('/timesheets/delete', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def delete_timesheet_f(self, **post):
        user = request.env.user
        timesheet_id = int(post.get('timesheet_id') or 0)

        employees = request.env['hr.employee'].sudo().search([
            ('user_id', '=', user.id)
        ])

        timesheet = request.env['account.analytic.line'].sudo().search([
            ('id', '=', timesheet_id),
            '|',
            ('user_id', '=', user.id),
            ('employee_id', 'in', employees.ids),
        ], limit=1)

        if not timesheet:
            return request.render('xsellence_portal.error_page', {
                'error_title': '❌ Delete Failed',
                'error_desc': 'Timesheet not found or you are not allowed to delete it.',
                'error_btn_label': 'View Timesheets',
                'error_btn_url': '/timesheets',
            })

        timesheet.unlink()

        return request.render('xsellence_portal.success_page', {
            'success_title': '✔️ Timesheet Deleted',
            'success_desc': 'Your timesheet entry has been deleted successfully.',
            'success_btn_label': 'View Timesheets',
            'success_btn_url': '/timesheets',
        })