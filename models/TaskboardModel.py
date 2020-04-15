from google.appengine.ext import ndb


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
            'updated_date': taskboard.updated_date.strftime('%Y-%m-%d')
        }

    @staticmethod
    def get_all_taskboards():
        return Taskboard.query().fetch()

    @staticmethod
    def fetch_taskboard(title, id=False):
        taskboard = Taskboard.query(Taskboard.title == title)
        if id:
            taskboard.filter(id != id)
        return taskboard.get()

    @staticmethod
    def update_taskboard(id, title, created_by):
        taskboard = Taskboard(id=id, title=title, created_by=created_by)
        taskboard.put()
        return taskboard

    @staticmethod
    def insert_taskboard(title, created_by):
        taskboard = Taskboard(title=title, created_by=created_by)
        if not TaskboardMethods.fetch_taskboard(title):
            taskboard.put()
        else:
            taskboard = False
        return taskboard

    @staticmethod
    def delete_taskboard(id):
        key = ndb.Key(Taskboard, id)
        key.delete()
