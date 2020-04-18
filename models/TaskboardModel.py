from google.appengine.ext import ndb

import models
from models.AppUserModel import AppUser, AppUserMethods

import datetime


class Taskboard(ndb.Model):
    title = ndb.StringProperty()
    created_by = ndb.KeyProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)


class TaskboardMethods:

    def __init__(self):
        pass

    @staticmethod
    def taskboard_to_dictionary(taskboard):

        return {
            'id': taskboard.key.id(),
            'title': taskboard.title,
            'created_by': taskboard.created_by.get().email,
            'created_date': taskboard.created_date.strftime('%Y-%m-%d'),
            'updated_date': taskboard.updated_date.strftime('%Y-%m-%d'),
            'creator': taskboard.created_by.get().email == AppUserMethods.get_current_user().email
        }

    @staticmethod
    def get_all_membered_taskboards(offset=0, limit=10):
        app_user_id = AppUserMethods.get_current_user().key.id()
        TaskboardMember = models.TaskboardMemberModel.TaskboardMember
        return TaskboardMember.query(
            TaskboardMember.app_user == ndb.Key(AppUser, app_user_id)).\
            fetch(projection=[TaskboardMember.taskboard])

    @staticmethod
    def get_all_authorised_taskboards():
        membered_taskboard_objects = TaskboardMethods.get_all_membered_taskboards()
        membered_taskboard_keys = map(lambda taskboardMember: taskboardMember.taskboard, membered_taskboard_objects)
        created_taskboard_keys = TaskboardMethods.get_all_created_taskboards()
        taskboard_keys = set(created_taskboard_keys).union(set(membered_taskboard_keys))
        taskboard_objects = TaskboardMethods.get_records_from_keys(taskboard_keys)
        return taskboard_objects

    @staticmethod
    def get_all_created_taskboards():
        app_user_key = AppUserMethods.get_current_user().key
        return Taskboard.query(Taskboard.created_by == app_user_key).fetch(keys_only=True)


    @staticmethod
    def get_by_id(id):
        id = int(str(id).strip())
        return Taskboard.get_by_id(id)

    @staticmethod
    def exists_taskboard(title, id=False):
        title = title.strip()
        taskboard = Taskboard.query(Taskboard.title == title)
        if id:
            id = int(str(id).strip())
            taskboard = taskboard.filter(Taskboard.key != ndb.Key(Taskboard, id))
        if taskboard:
            taskboard = taskboard.get()
        return bool(taskboard)

    @staticmethod
    def update_taskboard(id, title):
        id = int(str(id).strip())
        title = title.strip()
        taskboard = Taskboard.get_by_id(id)
        taskboard.title = title
        taskboard.updated_date = datetime.datetime.now()
        if not TaskboardMethods.exists_taskboard(title, id):
            taskboard.put()
        else:
            taskboard = False
        return taskboard

    @staticmethod
    def insert_taskboard(title):
        title = title.strip()
        taskboard = Taskboard(title=title, created_by=AppUserMethods.get_current_user().key)
        if not TaskboardMethods.exists_taskboard(title):
            taskboard.put()
            models.TaskboardMemberModel.TaskboardMemberMethods.insert_taskboard_member(taskboard.key.id(), taskboard.created_by.id())
        else:
            taskboard = False
        return taskboard

    @staticmethod
    def put_taskboard(title, id=None):
        return TaskboardMethods.update_taskboard(id, title) if id else TaskboardMethods.insert_taskboard(title)

    @staticmethod
    def delete_taskboard(id):
        id = int(str(id).strip())
        key = ndb.Key(Taskboard, id)
        key.delete()

    @staticmethod
    def get_records_from_keys(taskboard_keys):
        return ndb.get_multi(taskboard_keys)
        pass
