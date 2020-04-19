import jinja2
import os

"""
View class that renders view with jinja
"""
# @TODO Make this class singleton following singleton pattern


class ViewHandler:

    def __init__(self, response, base_url, user, login_out_url):
        self.template_values = {}
        self.jinja = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'views'))),
            extensions=['jinja2.ext.autoescape'],
            autoescape=True
        )
        self.response = response
        # base_url for application
        self.template_values["base_url"] = base_url
        # logged in user
        self.template_values["user"] = user
        # login logout url
        self.template_values["url"] = login_out_url
        self.template_values["title"] = "Task management"

    def render(self, template):
        self.response.write(self.jinja.get_template(template).render({'params': self.template_values}))


