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

    def post(self):
        params = json.loads(self.request.body)
        taskboard_object = TaskboardMethods.insert_taskboard(params['title'], self.appUser.key)
        if taskboard_object:
            response_object = TaskboardMethods.taskboard_to_dictionary(taskboard_object)
            response = {'success': True, 'data': response_object}
        else:
            response = {'success': False, 'message': 'Taskboard with same title already exists'}

        self.send_json_object(response)

    def put(self):
        pass

    def delete(self):
        pass
