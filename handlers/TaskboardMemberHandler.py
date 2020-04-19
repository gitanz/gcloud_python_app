from handlers.BaseHandler import BaseHandler
from models.TaskModel import TaskMethods
from models.TaskboardMemberModel import TaskboardMemberMethods
from models.TaskboardModel import *
import json

"""
    Taskboard member association relation request's handlers
    extends base handler
"""


class TaskboardMemberHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(TaskboardMemberHandler, self).__init__(request=request, response=response)

    def index(self, taskboard_id):
        """
            get all memebers of provided taskboard id
        :param taskboard_id:
        :return:
        """
        # check if current user has permission to get taskboard i.e taskboad appears in users permitted taskboard list
        if self.is_get_authorised(taskboard_id):
            # get all members
            members = TaskboardMemberMethods.get_all_taskboard_members_by_taskboard(taskboard_id)
            # initialise response dictionary
            response = {'success': True, 'data': []}
            # for each members append to response in way required by view
            for member in members:
                response['data'].append(TaskboardMemberMethods.taskboard_member_to_dictionary(member))
        else:
            # if not authorised, send unauthorised response
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    # return members of taskboard only if current user has permission to view this taskboard
    def is_get_authorised(self, id):
        """
        # return members of taskboard only if current user has permission to view this taskboard
        # current user can view this taskboard, only if this taskboard is in his authorised set of taskboard (i.e of which he is creator or member of)
        :param id:
        :return: boolean
        """

        # taskboard object fetched by ID
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        # get all authorised taskboardobjects of user
        authorised_taskboard_objects = TaskboardMethods.get_all_authorised_taskboards()
        # return true if this taskboard is in authorised taskboard object
        return taskboard_object in authorised_taskboard_objects

    def post(self):
        """
            Add member in taskboard
            i) check load request params,
            ii) check request valid and operation is permitted with validate() method
            iii) create TaskboardMember object for each user selected,
                and store in datastore

        :return:
        """
        params = json.loads(self.request.body)
        # validation and authorisation done in self.validate() method
        params, validation_errors = self.validate(params)
        # if validation errors send error response
        if validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            # create each app_user, taskboard object for taskmember and store.
            for app_user_id in params['app_user']:
                TaskboardMemberMethods.insert_taskboard_member(params['taskboard'], int(app_user_id))
            # create success response object
            response = {
                'success': True,
                'message': 'Successfully added selected users to board',
                'validate': True,
                'errors': False
            }
        # send json response.
        self.send_json_object(response)

    def delete(self):
        """
        Delete member from taskboard
        Deletion of member will result into assigned task as unassigned.
        :return:
        """

        # load json request in python object
        params = json.loads(self.request.body)

        # perfom authorisation,i.e, check if operation is carried out by board creator
        params, validation_errors = self.is_authorised(params)
        # creator should not be able to remove himself from board
        remove_user = params['app_user']
        taskboard = params['taskboard']

        # # admin is always a member
        # if TaskboardMethods.get_by_id(taskboard).created_by.id() == remove_user:
        #     validation_errors['unauthorised'] = True

        # if validation error, initialise failed response
        if validation_errors:
            response = {'success': False, 'validate': False, 'errors': validation_errors}
        else:
            # get associated tasks with taskboard_id and app_user_id
            associated_tasks_in_board = TaskMethods.get_all_tasks_by_taskboard_and_member(params['taskboard'],
                                                                                          params['app_user'])
            # first unaasign tasks
            TaskMethods.unassign_tasks(associated_tasks_in_board)

            # delete taskboard member method with provided taskboard and app_user
            TaskboardMemberMethods.delete_taskboard_member(params['taskboard'], params['app_user'])
            # create response dictionary for success
            response = {'success': True, 'validate': True, 'errors': validation_errors}
        # send response object
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
        """
        raise error if logged in user is not creator of taskboard.
        :param params:
        :param validation_error:
        :return: params, validation_error
        """
        if 'taskboard' in params and len(str(params['taskboard']).strip()) >= 0:

            taskboard = TaskboardMethods.get_by_id(int(params['taskboard']))
            # unauthorised if current user is not the creator
            if taskboard.created_by != AppUserMethods.get_current_user().key:
                validation_error = {'unauthorised': True}
        # return params, validation_error tuple.
        return params, validation_error
