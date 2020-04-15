#!/usr/bin/env python

from handlers.MainHandler import MainHandler
from handlers.TaskboardHandler import TaskboardHandler

import webapp2
app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/taskboards', handler=TaskboardHandler, name='home', handler_method="list", methods=['GET']),
    webapp2.Route('/taskboards', handler=TaskboardHandler, name='home', handler_method="post", methods=['POST']),
    ('/taskboard/(.+)', TaskboardHandler),
], debug=True)