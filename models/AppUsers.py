from google.appengine.ext import ndb
from google.appengine.api import users

class AppUsers(ndb.Model):
    email = ndb.StringProperty()


class AppUsersMethod:
    def __init__(self):
        pass

    @staticmethod
    def get_current_user():
        if users.get_current_user():
            return AppUsersMethod.fetch_user(users.get_current_user().email())
        else:
            return False

    @staticmethod
    def user_to_dictionary(app_user):
        return {'id': app_user.key.id(), 'email': app_user.email}

    @staticmethod
    def get_all_users():
        return AppUsers.query()

    @staticmethod
    def update_user(id, email):
        app_user = AppUsers(id=id, email=email)
        app_user.put()
        return app_user

    @staticmethod
    def insert_user(email):
        app_user = AppUsers(email=email)
        app_user.put()
        return app_user

    @staticmethod
    def delete_user(id):
        key = ndb.Key(AppUsers, id)
        key.delete()

    @staticmethod
    def fetch_user(email):
        app_user = AppUsers.query(AppUsers.email == email).get()
        if not app_user:
            app_user = AppUsersMethod.insert_user(email)
        return app_user
