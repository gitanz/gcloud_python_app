from handlers.BaseHandler import BaseHandler
from models.TaskboardMember import TaskboardMemberMethods
from models.TaskboardModel import *
import json


class TaskboardMemberHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskboardMemberHandler, self).__init__(request=request, response=response)

    def index(self, id):
        members = TaskboardMemberMethods.get_all_taskboard_members_by_taskboard(id)
        response = {'success': True, 'data': []}
        for member in members:
            response['data'].append(TaskboardMemberMethods.taskboard_member_to_dictionary(member))
        self.send_json_object(response)

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

    def validate(self, params):

        validation_error = {}
        # for taskboard
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
