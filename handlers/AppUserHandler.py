from handlers.BaseHandler import BaseHandler
from models.AppUserModel import *

"""
Controller class for App User.
Interacts with routes, AppUserModel and View 
"""


class AppUserHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(AppUserHandler, self).__init__(request=request, response=response)

    def index(self):
        """
            send all users as json string
        """
        # get all user records
        user_objects = AppUserMethods.get_all_users()
        # app_users list to hold formatted user_objects which will be sent as response
        app_users = []
        # map each user_objects to json format parsable by view
        for user_object in user_objects:
            # user object preparation for view
            response_object = AppUserMethods.user_to_dictionary(user_object)
            # add prepared user to app_users list
            app_users.append(response_object)
        # compile full response
        response = {'success': True, 'data': app_users}
        # send response as json
        self.send_json_object(response)

    def get(self, id):
        """
        accepts user id as id, returns json string object
        :param id:
        """
        # get user object
        user_object = AppUserMethods.get_user(int(id))
        # prepare data and compile response
        response = {'success': True, 'data': AppUserMethods.user_to_dictionary(user_object)}
        # send response as json
        self.send_json_object(response)
