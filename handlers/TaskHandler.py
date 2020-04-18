from handlers.BaseHandler import BaseHandler
from models.TaskModel import TaskMethods
from models.TaskboardModel import *

import json


class TaskHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskHandler, self).__init__(request=request, response=response)

    def index(self):
        task_objects = TaskMethods.get_all_tasks()
        tasks = []
        for task_object in task_objects:
            response_object = TaskMethods.task_to_dictionary(task_object)
            tasks.append(response_object)
        response = {'success': True, 'data': tasks}
        self.send_json_object(response)

    def get_all_taskboard_tasks(self, taskboard_id):
        if self.is_get_authorised(taskboard_id):
            task_objects = TaskMethods.get_all_tasks_by_taskboard(taskboard_id)
            tasks = []
            for task_object in task_objects:
                response_object = TaskMethods.task_to_dictionary(task_object)
                tasks.append(response_object)
            response = {'success': True, 'data': tasks}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    def is_get_authorised(self, id):
        if not id:
            return False
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        authorised_taskboard_objects = TaskboardMethods.get_all_authorised_taskboards()
        return taskboard_object in authorised_taskboard_objects

    def get(self, id):
        task_object = TaskMethods.get_by_id(int(id))
        if self.is_get_authorised(task_object.taskboard.id()):
            response = {'success': True, 'data': TaskMethods.task_to_dictionary(task_object)}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}
        self.send_json_object(response)

    def post(self):
        params = json.loads(self.request.body)
        params, validation_errors = self.validate(params)
        if not self.is_get_authorised(params['taskboard_id']):
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}
        elif validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            task_object = TaskMethods.put_task(
                params['taskboard_id'],
                params['title'],
                params['description'],
                params['due_date'],
                params['assigned_to'],
                params['status'],
                params['id']
            )
            response_object = TaskboardMethods.taskboard_to_dictionary(task_object)
            response = {
                'success': True,
                'message': 'Successfully updated task.' if params['id'] else 'Successfully added task.',
                'validate': True,
                'data': response_object,
                'errors': False
            }
        self.send_json_object(response)

    def mark_complete(self, task_id):
        params = json.loads(self.request.body)
        task = TaskMethods.get_by_id(params['id'])
        if self.is_get_authorised(task.taskboard.id()):
            TaskMethods.mark_as_complete(task_id)
            response = {'success': True}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    def mark_ongoing(self, task_id):
        params = json.loads(self.request.body)
        task = TaskMethods.get_by_id(params['id'])
        if self.is_get_authorised(task.taskboard.id()):
            TaskMethods.mark_as_ongoing(task_id)
            response = {'success': True}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    def delete_task(self, task_id):
        params = json.loads(self.request.body)
        task = TaskMethods.get_by_id(params['id'])
        if self.is_get_authorised(task.taskboard.id()):
            TaskMethods.delete_task(task.key.id())
            response = {'success': True}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)


    def validate(self, params):
        validation_error = {}
        if 'id' not in params:
            params['id'] = False

        if 'taskboard_id' not in params:
            params['taskboard_id'] = False

        if 'status' not in params:
            params['status'] = False
        else:
            params['status'] = params['status'] == '1'

        if 'title' not in params or len(params['title'].strip()) == 0:
            validation_error['title'] = 'Title field is required'

        if 'title' in params and len(params['title'].strip()) > 0:
            if bool(TaskMethods.exists_task(params['title'], params['id'])):
                validation_error['title'] = 'Title already exists'

        if 'taskboard_id' not in params or len(str(params['taskboard_id']).strip()) == 0:
            validation_error['title'] = 'No taskboard selected.'

        if 'description' not in params or len(params['description'].strip()) == 0:
            validation_error['description'] = 'Description field is required'

        if 'due_date' not in params or len(params['due_date'].strip()) == 0:
            validation_error['due_date'] = 'Due date field is required'

        if 'due_date' in params and len(params['due_date'].strip()) > 0:
            try:
                datetime.datetime.strptime(params['due_date'].strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                validation_error['due_date'] = 'Invalid date'

        if 'assigned_to' not in params or not params['assigned_to'] or len(str(params['assigned_to']).strip()) == 0:
            validation_error['assigned_to'] = 'Assigned to field is required'

        return params, validation_error
