from handlers.BaseHandler import BaseHandler


class MainHandler(BaseHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(MainHandler, self).__init__(request=request, response=response)

    def get(self):
        self.view.render("master.html")
