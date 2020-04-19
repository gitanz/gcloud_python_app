#!/usr/bin/env python
from handlers.AppUserHandler import AppUserHandler
from handlers.MainHandler import MainHandler
from handlers.TaskHandler import TaskHandler
from handlers.TaskboardHandler import TaskboardHandler
import webapp2
from handlers.TaskboardMemberHandler import TaskboardMemberHandler

# api routes
app = webapp2.WSGIApplication([
    # home page, renders master.html
    webapp2.Route('/', handler=MainHandler, name='home'),
    # get all authorised taskboards
    webapp2.Route(r'/taskboards', handler=TaskboardHandler, name='taskboard_index', handler_method="index", methods=['GET']),
    # get taskboard by id
    webapp2.Route(r'/taskboards/<:\d+>', handler=TaskboardHandler, name='taskboard', handler_method="get", methods=['GET']),
    # save/update taskboard
    webapp2.Route('/taskboards', handler=TaskboardHandler, name='taskboard_post', handler_method="post", methods=['POST']),
    # delete taskboard
    webapp2.Route('/taskboards/delete', handler=TaskboardHandler, name='taskboard_delete', handler_method="delete_taskboard", methods=['POST']),
    # get all users
    webapp2.Route('/app_users', handler=AppUserHandler, name='app_users_index', handler_method="index", methods=['GET']),
    # get user by id
    webapp2.Route(r'/app_users/<:\d+>', handler=AppUserHandler, name='app_user', handler_method="get", methods=['GET']),
    # add members to taskboard
    webapp2.Route('/taskboard_members', handler=TaskboardMemberHandler, name='taskboard_user_post', handler_method="post", methods=['POST']),
    # get all taskboard members
    webapp2.Route('/taskboard_members/<:\d+>', handler=TaskboardMemberHandler, name='taskboard_user_get', handler_method="index", methods=['GET']),
    # delete taskboard member
    webapp2.Route('/taskboard_members/delete', handler=TaskboardMemberHandler, name='taskboard_user_delete', handler_method="delete", methods=['POST']),
    # save/update post
    webapp2.Route('/tasks', handler=TaskHandler, name='task_post', handler_method="post", methods=['POST']),
    # get all taskboard tasks
    webapp2.Route(r'/taskboards/<:\d+>/tasks', handler=TaskHandler, name='taskboard_tasks', handler_method="get_all_taskboard_tasks", methods=['GET']),
    # get taskboard by id
    webapp2.Route('/tasks/<:\d+>', handler=TaskHandler, name='task_get', handler_method="get", methods=['GET']),
    # mark task as completed
    webapp2.Route('/tasks/<:\d+>/mark-complete', handler=TaskHandler, name='task_complete', handler_method="mark_complete", methods=['POST']),
    # mark task as ongoing
    webapp2.Route('/tasks/<:\d+>/mark-ongoing', handler=TaskHandler, name='task_ongoing', handler_method="mark_ongoing", methods=['POST']),
    # delete task
    webapp2.Route('/tasks/<:\d+>/delete', handler=TaskHandler, name='task_delete', handler_method="delete_task", methods=['POST'])

], debug=True)
