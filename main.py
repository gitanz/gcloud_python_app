#!/usr/bin/env python
from handlers.AppUserHandler import AppUserHandler
from handlers.MainHandler import MainHandler
from handlers.TaskHandler import TaskHandler
from handlers.TaskboardHandler import TaskboardHandler
import webapp2
from handlers.TaskboardMemberHandler import TaskboardMemberHandler

app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route(r'/taskboards', handler=TaskboardHandler, name='taskboard_index', handler_method="list", methods=['GET']),
    webapp2.Route(r'/taskboards/<:\d+>', handler=TaskboardHandler, name='taskboard', handler_method="get", methods=['GET']),
    webapp2.Route('/taskboards', handler=TaskboardHandler, name='taskboard_post', handler_method="post", methods=['POST']),
    webapp2.Route('/app_users', handler=AppUserHandler, name='app_users_index', handler_method="list", methods=['GET']),
    webapp2.Route(r'/app_users/<:\d+>', handler=AppUserHandler, name='app_user', handler_method="get", methods=['GET']),
    webapp2.Route('/taskboard_members', handler=TaskboardMemberHandler, name='taskboard_user_post', handler_method="post", methods=['POST']),
    webapp2.Route('/taskboard_members/<:\d+>', handler=TaskboardMemberHandler, name='taskboard_user_get', handler_method="index", methods=['GET']),
    webapp2.Route('/tasks', handler=TaskHandler, name='task_post', handler_method="post", methods=['POST']),
], debug=True)
