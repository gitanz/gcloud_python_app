from handlers.BaseHandler import BaseHandler
from models.TaskModel import TaskMethods
from models.TaskboardModel import *

import json

"""
Tasks request handler
extends base handler
"""


class TaskHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskHandler, self).__init__(request=request, response=response)

    def index(self):
        # get all tasks
        task_objects = TaskMethods.get_all_tasks()
        # create tasks object
        tasks = []
        # append each taskobjects into tasks in format readble by view
        for task_object in task_objects:
            # taskobject to view object
            response_object = TaskMethods.task_to_dictionary(task_object)
            tasks.append(response_object)
        response = {'success': True, 'data': tasks}
        self.send_json_object(response)

    def get_all_taskboard_tasks(self, taskboard_id):
        """
        get all tasks for a particular taskboard
        :param taskboard_id:
        """
        # authorise if user is member.
        if self.is_get_authorised(taskboard_id):
            # fetch task's from Task datastore
            task_objects = TaskMethods.get_all_tasks_by_taskboard(taskboard_id)
            # initialise empty task list
            tasks = []
            # resolve taskobject into format required in view, append into tasks list
            for task_object in task_objects:
                response_object = TaskMethods.task_to_dictionary(task_object)
                tasks.append(response_object)
            #     create response object with data
            response = {'success': True, 'data': tasks}
        else:
            # create failure response object
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
        """
            Validate task form
        """
        # initialise validation error dict.
        validation_error = {}
        # assign id:false in params if not
        if 'id' not in params:
            params['id'] = False
        # assign taskbaord_id:false in params if not set
        if 'taskboard_id' not in params:
            params['taskboard_id'] = False

        # assign status:incomplete(false) if not
        if 'status' not in params:
            params['status'] = False
        else:
            # status is complete(=true) if status is 1
            params['status'] = params['status'] == '1'

        # validation field for title
        if 'title' not in params or len(params['title'].strip()) == 0:
            validation_error['title'] = 'Title field is required'
        # checking if title already exists
        if 'title' in params and len(params['title'].strip()) > 0:
            if bool(TaskMethods.exists_task(params['title'], params['id'])):
                validation_error['title'] = 'Title already exists'
        # validation if taskboard_id is set in form
        if 'taskboard_id' not in params or len(str(params['taskboard_id']).strip()) == 0:
            validation_error['title'] = 'No taskboard selected.'
        # description field required
        if 'description' not in params or len(params['description'].strip()) == 0:
            validation_error['description'] = 'Description field is required'
        # due_date filed required check
        if 'due_date' not in params or len(params['due_date'].strip()) == 0:
            validation_error['due_date'] = 'Due date field is required'
        # due_date field date_time valid check
        if 'due_date' in params and len(params['due_date'].strip()) > 0:
            try:
                datetime.datetime.strptime(params['due_date'].strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
            except:
                validation_error['due_date'] = 'Invalid date'
        # assigned_to field required check
        if 'assigned_to' not in params or not params['assigned_to'] or len(str(params['assigned_to']).strip()) == 0:
            validation_error['assigned_to'] = 'Assigned to field is required'

        return params, validation_error
