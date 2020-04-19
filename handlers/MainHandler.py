from handlers.BaseHandler import BaseHandler

"""
returns home page template
"""


class MainHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(MainHandler, self).__init__(request=request, response=response)

    def get(self):
        # with view object of ViewHandler created in BaseHandler, render master.html
        self.view.render("master.html")
