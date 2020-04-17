from google.appengine.ext import ndb
from models.AppUserModel import AppUserMethods
import datetime

from models.TaskboardModel import TaskboardMethods


class Task(ndb.Model):
    taskboard = ndb.KeyProperty()
    title = ndb.StringProperty()
    description = ndb.TextProperty()
    due_date = ndb.DateTimeProperty()
    assigned_to = ndb.KeyProperty()
    status = ndb.BooleanProperty()
    created_by = ndb.KeyProperty()
    created_date = ndb.DateTimeProperty(auto_now=True)
    updated_date = ndb.DateTimeProperty(auto_now=True)


class TaskMethods:

    def __init__(self):
        pass

    @staticmethod
    def task_to_dictionary(task):
        return {
            'id': task.key.id(),
            'taskboard_id': task.taskboard.id(),
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d'),
            'assigned_to_email': task.assigned_to.get().email,
            'assigned_to': task.assigned_to.get().key.id(),
            'status': task.status,
            'created_by': task.created_by.get().email,
            'created_date': task.created_date.strftime('%Y-%m-%d'),
            'updated_date': task.updated_date.strftime('%Y-%m-%d'),
            'creator': task.created_by.get().email == AppUserMethods.get_current_user().email
        }

    @staticmethod
    def get_all_tasks():
        return Task.query().fetch()

    @staticmethod
    def get_all_tasks_by_taskboard(taskboard_id):
        taskboard_id = int(str(taskboard_id).strip())
        taskboard_key = TaskboardMethods.get_by_id(taskboard_id).key
        return Task.query(Task.taskboard == taskboard_key).fetch()

    @staticmethod
    def get_by_id(id):
        id = int(str(id).strip())
        return Task.get_by_id(id)

    @staticmethod
    def exists_task(title, id=False):
        title = title.strip()
        task = Task.query(Task.title == title)
        if id:
            id = int(str(id).strip())
            task = task.filter(Task.key != ndb.Key(Task, id))
        if task:
            task = task.get()
        return bool(task)

    @staticmethod
    def update_task(id, title, description, due_date, assigned_to, status):
        id = int(str(id).strip())
        title = title.strip()
        task = Task.get_by_id(id)
        task.title = title.strip()
        task.description = description.strip()
        task.due_date = datetime.datetime.strptime(due_date.strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
        task.assigned_to = AppUserMethods.get_user_key(int(assigned_to))
        task.status = bool(status)
        task.updated_date = datetime.datetime.now()

        if not TaskMethods.exists_task(title, id):
            task.put()
        else:
            task = False
        return task

    @staticmethod
    def insert_task(taskboard_id, title, description, due_date, assigned_to):
        task = Task()
        task.taskboard = TaskboardMethods.get_by_id(taskboard_id).key
        task.title = title.strip()
        task.description = description.strip()
        task.due_date = datetime.datetime.strptime(due_date.strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
        task.assigned_to = AppUserMethods.get_user_key(int(assigned_to))
        task.status = False
        task.updated_date = datetime.datetime.now()
        task.created_date = datetime.datetime.now()
        task.created_by = AppUserMethods.get_current_user().key

        if not TaskMethods.exists_task(title):
            task.put()
        else:
            task = False
        return task

    @staticmethod
    def put_task(taskboard_id, title, description, due_date, assigned_to, status=None, id=None):
        return TaskMethods.update_task(id, title, description, due_date, assigned_to, status) if id \
            else TaskMethods.insert_task(taskboard_id, title, description, due_date, assigned_to)

    @staticmethod
    def delete_task(id):
        id = int(str(id).strip())
        key = ndb.Key(Task, id)
        key.delete()
