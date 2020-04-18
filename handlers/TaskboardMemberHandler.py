from handlers.BaseHandler import BaseHandler
from models.TaskModel import TaskMethods
from models.TaskboardMemberModel import TaskboardMemberMethods
from models.TaskboardModel import *
import json


class TaskboardMemberHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskboardMemberHandler, self).__init__(request=request, response=response)

    def index(self, taskboard_id):
        if self.is_get_authorised(taskboard_id):
            members = TaskboardMemberMethods.get_all_taskboard_members_by_taskboard(taskboard_id)
            response = {'success': True, 'data': []}
            for member in members:
                response['data'].append(TaskboardMemberMethods.taskboard_member_to_dictionary(member))
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    def is_get_authorised(self, id):
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        authorised_taskboard_objects = TaskboardMethods.get_all_authorised_taskboards()
        return taskboard_object in authorised_taskboard_objects

    def post(self):
        params = json.loads(self.request.body)
        params, validation_errors = self.validate(params)
        if validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            for app_user_id in params['app_user']:
                TaskboardMemberMethods.insert_taskboard_member(params['taskboard'], int(app_user_id))

            response = {
                'success': True,
                'message': 'Successfully added selected users to board',
                'validate': True,
                'errors': False
            }

        self.send_json_object(response)

    def delete(self):
        params = json.loads(self.request.body)
        params, validation_errors = self.is_authorised(params)
        # creator should not be able to remove himself from board
        remove_user = params['app_user']
        taskboard = params['taskboard']

        # # admin is always a member
        # if TaskboardMethods.get_by_id(taskboard).created_by.id() == remove_user:
        #     validation_errors['unauthorised'] = True

        if validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            associated_tasks_in_board = TaskMethods.get_all_tasks_by_taskboard_and_member(params['taskboard'],
                                                                                          params['app_user'])
            TaskMethods.unassign_tasks(associated_tasks_in_board)
            TaskboardMemberMethods.delete_taskboard_member(params['taskboard'], params['app_user'])
            response = {'success': True, 'validate': True, 'errors': validation_errors}

        self.send_json_object(response)

    def validate(self, params):

        validation_error = {}

        params, validation_error = self.is_authorised(params, validation_error)

        if 'taskboard' not in params or len(str(params['taskboard']).strip()) == 0:
            validation_error = {'user': 'Taskboard not selected.'}

        if 'app_user' not in params or len(params['app_user']) == 0:
            validation_error = {'user': 'Select users to invite.'}

        if 'app_user' in params and len(params['app_user']) and 'taskboard' in params and len(
                str(params['taskboard']).strip()):
            for app_user_id in params['app_user']:
                if TaskboardMemberMethods.exists_relation(params['taskboard'], app_user_id):
                    validation_error = {'user': AppUserMethods.get_user(app_user_id).email + " is already a member"}

        return params, validation_error

    def is_authorised(self, params, validation_error={}):
        if 'taskboard' in params and len(str(params['taskboard']).strip()) >= 0:
            # validate if user can perform insert
            taskboard = TaskboardMethods.get_by_id(int(params['taskboard']))
            if taskboard.created_by != AppUserMethods.get_current_user().key:
                validation_error = {'unauthorised': True}

        return params, validation_error
