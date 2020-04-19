from google.appengine.ext import ndb
from models.AppUserModel import AppUserMethods, AppUser
from models.TaskboardModel import Taskboard

"""
    TaskboardMember association table
    This table contains associaion within taskboard and User key
    Each association/record implies that user is member of the taskboard
    
    taskboard: holds key of taskboard
    app_user: holds key of associated member object from AppUserModel
    created_date: date of association made.
"""


class TaskboardMember(ndb.Model):
    taskboard = ndb.KeyProperty()
    app_user = ndb.KeyProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)


"""
    TaskboardMemberMethods
    Helper method for TaskboardMemberModel
"""


class TaskboardMemberMethods:

    def __init__(self):
        pass

    @staticmethod
    def taskboard_member_to_dictionary(taskboard_member):
        # return taskboard_member association to view in required format
        return {
            'id': taskboard_member.key.id(),
            'taskboard': taskboard_member.taskboard.id(),
            'app_user': taskboard_member.app_user.id(),
            'taskboard_title': taskboard_member.taskboard.get().title,
            'app_user_email': taskboard_member.app_user.get().email,
            'created_date': taskboard_member.created_date.strftime('%Y-%m-%d')
        }

    @staticmethod
    def get_all_taskboard_members_by_taskboard(taskboard_id):
        """
        return all members from taskboard given the taskboard id
        :param taskboard_id:
        :return:
        """
        # parse taskboard as int
        taskboard_id = int(str(taskboard_id).strip())
        # get all taskboards member with taskboard id
        return TaskboardMember.query(TaskboardMember.taskboard == ndb.Key(Taskboard, taskboard_id)).fetch()

    @staticmethod
    def get_all_taskboards_by_taskboard_member(app_user_id):
        """
        return all records from taskboards given the app_user_id
        :param app_user_id:
        :return:
        """
        app_user_id = int(str(app_user_id).strip())
        return TaskboardMember.query(TaskboardMember.app_user == ndb.Key(AppUser, app_user_id)).fetch()

    @staticmethod
    def exists_relation(taskboard_id, app_user_id):
        """Check if there is already a relation between taksboard_id and app_user_id"""
        app_user_id = int(str(app_user_id).strip())
        taskboard_id = int(str(taskboard_id).strip())
        taskboard = ndb.Key(Taskboard, taskboard_id)
        app_user = ndb.Key(AppUser, app_user_id)
        return TaskboardMember.query(TaskboardMember.taskboard == taskboard).filter(
            TaskboardMember.app_user == app_user).get()

    @staticmethod
    def insert_taskboard_member(taskboard_id, app_user_id):
        """
        insert taskboard and member association in datastore
        :param taskboard_id:
        :param app_user_id:
        :return:
        """
        app_user_id = int(str(app_user_id).strip())
        taskboard_id = int(str(taskboard_id).strip())
        taskboard = ndb.Key(Taskboard, taskboard_id)
        app_user = ndb.Key(AppUser, app_user_id)
        taskboard_member = TaskboardMember(taskboard=taskboard, app_user=app_user)
        if not TaskboardMemberMethods.exists_relation(taskboard_id, app_user_id):
            return taskboard_member.put()
        else:
            return False

    @staticmethod
    def delete_taskboard_member(taskboard_id, app_user_id):
        """
        Delete taskboard member matching asscoiation taskboard_id ->app_user_id
        :param taskboard_id:
        :param app_user_id:
        :return:
        """
        app_user_id = int(str(app_user_id).strip())
        taskboard_id = int(str(taskboard_id).strip())
        # delete record with key if association exists
        taskboard_member_relation = TaskboardMemberMethods.exists_relation(taskboard_id, app_user_id)
        if not taskboard_member_relation:
            return False
        else:
            taskboard_member_relation.key.delete()
            return True
