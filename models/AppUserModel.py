from google.appengine.ext import ndb
from google.appengine.api import users


# AppUser Model
# consists email as string property
class AppUser(ndb.Model):
    email = ndb.StringProperty()


"""
AppUserMethods 
Helper methods for AppUserModel
"""


class AppUserMethods:
    def __init__(self):
        pass
    # get's current user
    @staticmethod
    def get_current_user():
        if users.get_current_user():
            # if user is logged in fetch current user that matches email
            return AppUserMethods.fetch_user(users.get_current_user().email())
        else:
            return False

    @staticmethod
    def user_to_dictionary(app_user):
        # user object in view readble format
        return {'id': app_user.key.id(), 'email': app_user.email}

    @staticmethod
    def get_all_users():
        # all user list shown to add Member in taskboard
        return AppUser.query().fetch()

    @staticmethod
    def update_user(id, email):
        # update user provided id and email
        app_user = AppUser(id=id, email=email)
        app_user.put()
        return app_user

    @staticmethod
    def insert_user(email):
        # insert user provided email
        app_user = AppUser(email=email)
        app_user.put()
        return app_user

    @staticmethod
    def get_user_key(id):
        # get user key, provided id
        id = int(id)
        key = ndb.Key(AppUser, id)
        return key

    @staticmethod
    def get_user(id):
        # get user provided id
        id = int(id)
        key = ndb.Key(AppUser, id)
        return key.get()

    @staticmethod
    def delete_user(id):
        # delete user from datastore
        key = ndb.Key(AppUser, id)
        key.delete()

    @staticmethod
    def fetch_user(email):
        # get user, if not in datastore, first add and then get
        app_user = AppUser.query(AppUser.email == email).get()
        if not app_user:
            app_user = AppUserMethods.insert_user(email)
        return app_user
