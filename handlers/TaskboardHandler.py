from handlers.BaseHandler import BaseHandler
from models.TaskboardModel import *
import json


class TaskboardHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskboardHandler, self).__init__(request=request, response=response)

    def list(self):
        taskboard_objects = TaskboardMethods.get_all_taskboards()
        taskboards = []
        for taskboard_object in taskboard_objects:
            response_object = TaskboardMethods.taskboard_to_dictionary(taskboard_object)
            taskboards.append(response_object)
        response = {'success': True, 'data': taskboards}
        self.send_json_object(response)

    def get(self, id):
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        response = {'success': True, 'data': TaskboardMethods.taskboard_to_dictionary(taskboard_object)}
        self.send_json_object(response)

    def post(self):
        params = json.loads(self.request.body)
        params, validation_errors = self.validate(params)
        if validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            taskboard_object = TaskboardMethods.put_taskboard(params['title'], params['id'])
            response_object = TaskboardMethods.taskboard_to_dictionary(taskboard_object)
            response = {
                'success': True,
                'message': 'Successfully updated taskboard.' if params['id'] else 'Successfully added taskboard.',
                'validate': True,
                'data': response_object,
                'errors': False
            }

        self.send_json_object(response)

    @staticmethod
    def validate(params):
        validation_error = {}
        if 'id' not in params:
            params['id'] = False

        if 'title' not in params or len(params['title'].strip()) == 0:
            validation_error = {'title': 'Please fill title'}

        if 'title' in params and len(params['title'].strip()) > 0:
            if bool(TaskboardMethods.exists_taskboard(params['title'], params['id'])):
                validation_error = {'title': 'Title already exists'}

        return params, validation_error
