from handlers.BaseHandler import BaseHandler
from models.TaskboardModel import *
import json

"""
    All taskboard related requests are directed to this handler
    extends BaseHandler
"""


class TaskboardHandler(BaseHandler):

    def __init__(self, request, response):
        """
        Constructor. Accepts request and response object. Calls BaseHandler constructor
        :param request:
        :param response:
        """
        # calling super class constructor
        super(TaskboardHandler, self).__init__(request=request, response=response)

    def index(self):
        """
            Gets all taskboards (i.e user's created + user's related) for taskboard index page
                i) get all authorised taskboard's raw objects
                ii) map each taskboard objects into form needed in view.
                This is done using taskboard_to_dictionary method in TaskboardModel helper methods
                iii) send back json requests
        """
        authorised_taskboard_objects = TaskboardMethods.get_all_authorised_taskboards()
        taskboards = []
        for taskboard_object in authorised_taskboard_objects:
            if taskboard_object:
                response_object = TaskboardMethods.taskboard_to_dictionary(taskboard_object)
                taskboards.append(response_object)

        response = {'success': True, 'data': taskboards}
        self.send_json_object(response)

    def get(self, id):
        """
        Gets particular taskboard for taskboard view page
            i) get taskboard's object by id
            ii) validate if current user is authorised to view the taskboard.
                i.e, current user should either be the creator or be a member of taskboard.
            iii) if authorised, send all fetched data as response with key 'success': True
                 else send response with key 'success': False and unauthorised:True
        :param id:
        """
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        if self.is_get_authorised(id):
            response = {'success': True, 'data': TaskboardMethods.taskboard_to_dictionary(taskboard_object)}
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}
        self.send_json_object(response)

    def is_get_authorised(self, id):
        """
        Checks if logged in user can access taskboard or not
        :param id: Taskboard id
        :return: Boolean (if taskboard is in list of taskboards that current user can view
        """
        taskboard_object = TaskboardMethods.get_by_id(int(id))
        authorised_taskboard_objects = TaskboardMethods.get_all_authorised_taskboards()
        return taskboard_object in authorised_taskboard_objects

    def post(self):
        """
        Save or update taskboard
            i) first check if user can save/edit taskboard
            ii) if user is authorised to perform operation,
                a) validate the post form,
                b) put(update if exists else insert) taskboard
            iii) create response message considering validation and authorisation responses
            iv) send json string as response
        """

        params = json.loads(self.request.body)
        if self.is_post_authorised(params):
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
        else:
            response = {'success': False, 'data': [], 'errors': {'unauthorised': True}}

        self.send_json_object(response)

    def is_post_authorised(self, params):
        """
        check if save or update taskboard is authorised for current user

            i) anyone can create a board. So, return true in Create Board operation
                i.e, if id field is not in params
            ii) if edit operation i.e, id is present, check if user is creator or member of the taskboard.

        :param params request parameters with taskboard id and title
        :return: boolean if save or update task is authorised for current user
        """
        if 'id' not in params or not params['id']:
            return True
        else:
            return self.is_get_authorised(params['id'])

    def validate(self, params):
        """
        Validate for title required field and title already exists

        :param params: (taskboard id and title)
        :return: validation error dictionary
        """
        validation_error = {}
        if 'id' not in params:
            params['id'] = False

        # if title field not set or is empty
        if 'title' not in params or len(params['title'].strip()) == 0:
            validation_error = {'title': 'Title field required'}

        # if title is set but title is already set for another taskboard.
        if 'title' in params and len(params['title'].strip()) > 0:
            # checking if taskboard already exists
            if bool(TaskboardMethods.exists_taskboard(params['title'], params['id'])):
                validation_error = {'title': 'Title already exists'}

        return params, validation_error

    def delete_taskboard(self):
        """
            delete taskboard from taskboard page.
            i) validate request and authenticate before operation
            ii) if taskboard not set, add error
            iii) load taskboard, if not loaded add error
            iv) if loaded, authenticate creator
            v) if creator not authenticated raise error
            vi) check if taskboard has no members,and tasks, raise error if any is yes
            vi) if error raised, cancel operation. else delete

        """
        # json to python object
        params = json.loads(self.request.body)
        # initializing validation,response and taskboard
        validation_error = {}
        response = {}
        taskboard = False
        # check if request has taskboard id
        if 'taskboard_id' not in params:
            validation_error['errors'] = 'No taskboard selected'
        else:
            # if taskboard id present, load taskboard from taskboard helper
            taskboard = TaskboardMethods.get_by_id(params['taskboard_id'])
        # if no taskboard present load error
        if not taskboard:
            validation_error['errors'] = "Taskboard could not be deleted."
        # if taskboard's creator is not current user, raise unathorised error
        if taskboard and taskboard.created_by != AppUserMethods.get_current_user().key and not validation_error:
            validation_error['unauthorised'] = True
        # if no validation error and user is creator, check if taskboard is empty
        elif not validation_error and taskboard and taskboard.created_by == AppUserMethods.get_current_user().key and not TaskboardMethods.is_empty(
                taskboard):
            # if taskboard is not empty, raise error
            validation_error['errors'] = "Taskboard not empty."
        # if no error raised, set success
        if not validation_error:
            TaskboardMethods.delete_taskboard(taskboard.key.id())
            response['success'] = True
        # if error raised, set error
        response['errors'] = validation_error if validation_error else False
        # send response as json string.
        self.send_json_object(response)
