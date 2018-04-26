from google.appengine.ext import ndb


class Message(ndb.Model):
    user = ndb.StringProperty()
    reciver = ndb.StringProperty()
    text = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)