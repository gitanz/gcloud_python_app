import webapp2
from google.appengine.api import users
from views.ViewHandler import ViewHandler
from models.AppUsers import *
import urlparse
import json

class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        # calling super class constructor
        super(BaseHandler, self).__init__(request=request, response=response)
        # initializing user property with current user. Returns None if not logged in
        self.user = users.get_current_user()
        # parsing request url for obtaining base url
        parsed = urlparse.urlparse(self.request.url)
        base_url = urlparse.urlunparse((parsed.scheme, parsed.netloc, "", "", "", ""))

        # creating login/logout url
        if self.user:
            url = users.create_logout_url(self.request.uri)
            self.appUser = AppUsersMethod.fetch_user(self.user.email())
        else:
            self.appUser = None
            url = users.create_login_url(self.request.uri)
            self.redirect(url)

        # default template values common for all templates.
        self.view = ViewHandler(self.response, base_url, self.user, url)

    def send_json_object(self, response_object):
        self.response.headers['content-type'] = 'text/plain'
        self.response.write(json.dumps(response_object))