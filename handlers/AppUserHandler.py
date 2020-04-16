from handlers.BaseHandler import BaseHandler
from models.AppUserModel import *


class AppUserHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(AppUserHandler, self).__init__(request=request, response=response)

    def list(self):
        user_objects = AppUserMethods.get_all_users()
        app_users = []
        for user_object in user_objects:
            response_object = AppUserMethods.user_to_dictionary(user_object)
            app_users.append(response_object)
        response = {'success': True, 'data': app_users}
        self.send_json_object(response)

    def get(self, id):
        user_object = AppUserMethods.get_user(int(id))
        response = {'success': True, 'data': AppUserMethods.user_to_dictionary(user_object)}
        self.send_json_object(response)
