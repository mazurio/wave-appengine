import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APIAnnouncement(messages.Message):
	module = messages.StringField(1, required = True)
	user = messages.StringField(2, required = True)

	title = messages.StringField(3, required = True)
	description = messages.StringField(4, required = True)
	timestamp = messages.IntegerField(5, required = True)

class APIAnnouncementList(messages.Message):
	list = messages.MessageField(APIAnnouncement, 1, repeated = True)

class Announcement(ndb.Model):
	_use_memcache = False
	_use_cache = False
	module = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)
	title = ndb.StringProperty(required = True)
	description = ndb.StringProperty(required = True)
	timestamp = ndb.IntegerProperty(required = True)