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
        task_objects = TaskMethods.get_all_tasks_by_taskboard(taskboard_id)
        tasks = []
        for task_object in task_objects:
            response_object = TaskMethods.task_to_dictionary(task_object)
            tasks.append(response_object)
        response = {'success': True, 'data': tasks}
        self.send_json_object(response)


    def get(self, id):
        task_object = TaskMethods.get_by_id(int(id))
        response = {'success': True, 'data': TaskMethods.task_to_dictionary(task_object)}
        self.send_json_object(response)

    def post(self):
        params = json.loads(self.request.body)
        params, validation_errors = self.validate(params)

        if validation_errors:
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

    def delete(self):
        pass

    def validate(self, params):
        validation_error = {}
        if 'id' not in params:
            params['id'] = False

        if 'status' not in params:
            params['status'] = False
        else:
            params['status'] = params['status'] == '1'

        if 'title' not in params or len(params['title'].strip()) == 0:
            validation_error['title'] = 'Title field is required'

        if 'title' in params and len(params['title'].strip()) > 0:
            if bool(TaskMethods.exists_task(params['title'], params['id'])):
                validation_error['title'] = 'Title already exists'

        if 'description' not in params or len(params['description'].strip()) == 0:
            validation_error['description'] = 'Description field is required'

        if 'due_date' not in params or len(params['due_date'].strip()) == 0:
            validation_error['due_date'] = 'Due date field is required'

        if 'due_date' in params and len(params['due_date'].strip()) > 0:
            try:
                datetime.datetime.strptime(params['due_date'].strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                validation_error['due_date'] = 'Invalid date'

        if 'assigned_to' not in params or len(str(params['assigned_to']).strip()) == 0:
            validation_error['assigned_to'] = 'Assigned to field is required'

        return params, validation_error
