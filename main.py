#!/usr/bin/env python
import os
import jinja2
import webapp2
from google.appengine.api import users
from model import Message
import json
from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user

        return self.render_template("home.html", params=params)

class NewMessageHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
        return self.render_template("new.html", params=params)

    def post(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        input_reciver = self.request.get("address")
        input_text = self.request.get("subject")
        params = {'user': user,
                  'text': input_text,
                  'reciver': input_reciver}
        if user:
            params['user'] = user
            message = Message(text=input_text, reciver=input_reciver, user=user.email())
            message.put()

        return self.render_template("new.html", params=params)

class SentMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            sent = Message().query(Message.user == user.email()).fetch()
            params['messages'] = sent
        return self.render_template("sent.html", params=params)

class InboxMessagesHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            sent = Message().query(Message.reciver == user.email()).fetch()
            params['messages'] = sent
        return self.render_template("inbox.html", params=params)

class SingleMessageHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            message = Message.get_by_id(int(message_id))
            params['message'] = message
        return self.render_template("message.html", params=params)

class DeleteMessageHandler(BaseHandler):
    def get(self, message_id):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            message = Message.get_by_id(int(message_id))
            params['message'] = message
        return self.render_template('delete-message.html', params=params)

    def post(self, message_id):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            message = Message.get_by_id(int(message_id))
            message.key.delete()
        return self.redirect_to('all')

class AllMessagesDeleteHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            messages = Message.query().fetch()
            params['messages'] = messages
            params["user"] = user
        return self.render_template("delete.html", params=params)

class WeatherHandler(BaseHandler):
    def get(self):
        user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        params = {
            'login': login_url,
            'logout': logout_url
        }
        if user:
            params['user'] = user
            data = urlfetch.fetch('http://api.openweathermap.org/data/2.5/weather?q=Zagreb&units=metric&appid=f8eed8b27db9beed8f29d78962b56497')
            weather = json.loads(data.content)
            params['weather'] = weather
        return self.render_template('weather.html', params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/new', NewMessageHandler),
    webapp2.Route('/sent', SentMessagesHandler),
    webapp2.Route('/inbox', InboxMessagesHandler),
    webapp2.Route('/delete', AllMessagesDeleteHandler, name='all'),
    webapp2.Route('/message/<message_id:\d+>', SingleMessageHandler),
    webapp2.Route('/message/<message_id:\d+>/delete', DeleteMessageHandler),
    webapp2.Route('/weather', WeatherHandler)
], debug=True)
