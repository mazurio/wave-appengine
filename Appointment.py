import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APIAppointment(messages.Message):
	# id
	timestamp = messages.IntegerField(1, required = True)
	title = messages.StringField(2, required = True)
	description = messages.StringField(3, required = True)
	status = messages.StringField(4, required = True)
	sender = messages.StringField(5, required = True)
	receiver = messages.StringField(6, required = True)
	date = messages.IntegerField(7, required = True)

class APIAppointmentList(messages.Message):
	list = messages.MessageField(APIAppointment, 1, repeated = True)

class Appointment(ndb.Model):
	_use_memcache = False
	_use_cache = False
	timestamp = ndb.IntegerProperty(required = True)
	title = ndb.StringProperty(required = True)
	description = ndb.StringProperty(required = True)
	status = ndb.StringProperty(required = True)
	sender = ndb.StringProperty(required = True)
	receiver = ndb.StringProperty(required = True)
	date = ndb.IntegerProperty(required = True)