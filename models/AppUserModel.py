from google.appengine.ext import ndb
from google.appengine.api import users


class AppUser(ndb.Model):
    email = ndb.StringProperty()


class AppUserMethods:
    def __init__(self):
        pass

    @staticmethod
    def get_current_user():
        if users.get_current_user():
            return AppUserMethods.fetch_user(users.get_current_user().email())
        else:
            return False

    @staticmethod
    def user_to_dictionary(app_user):
        return {'id': app_user.key.id(), 'email': app_user.email}

    @staticmethod
    def get_all_users():
        return AppUser.query().fetch()

    @staticmethod
    def update_user(id, email):
        app_user = AppUser(id=id, email=email)
        app_user.put()
        return app_user

    @staticmethod
    def insert_user(email):
        app_user = AppUser(email=email)
        app_user.put()
        return app_user

    @staticmethod
    def get_user_key(id):
        id = int(id)
        key = ndb.Key(AppUser, id)
        return key

    @staticmethod
    def get_user(id):
        id = int(id)
        key = ndb.Key(AppUser, id)
        return key.get()

    @staticmethod
    def delete_user(id):
        key = ndb.Key(AppUser, id)
        key.delete()

    @staticmethod
    def fetch_user(email):
        app_user = AppUser.query(AppUser.email == email).get()
        if not app_user:
            app_user = AppUserMethods.insert_user(email)
        return app_user
