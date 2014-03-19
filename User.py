import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APIUser(messages.Message):
	username = messages.StringField(1, required = True)
	photo = messages.StringField(2, required = True)
	firstname = messages.StringField(3, required = True)
	lastname = messages.StringField(4, required = True)
	description = messages.StringField(5, required = True)
	email = messages.StringField(6, required = True)
	phone = messages.StringField(7, required = True)

class APIUserList(messages.Message):
	list = messages.MessageField(APIUser, 1, repeated = True)

class User(ndb.Model):
	username = ndb.StringProperty(required = True)
	password = ndb.StringProperty(required = True)
	photo = ndb.StringProperty(required = True)
	firstname = ndb.StringProperty(required = True)
	lastname = ndb.StringProperty(required = True)
	description = ndb.StringProperty(required = True)
	email = ndb.StringProperty(required = True)
	phone = ndb.StringProperty(required = True)

class UserSync(ndb.Model):
	contact = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)

#
# Create users:
#
damian = User(
	key = ndb.Key(User, 'd.mazurkiewicz'),
	username = 'd.mazurkiewicz',
	password = 'password',
	photo = 'http://i.imgur.com/7J39xOE.jpg',
	firstname = 'Damian',
	lastname = 'Mazurkiewicz',
	description = 'student',
	email = 'd.mazurkiewicz@lancaster.ac.uk',
	phone = '+44 075 0097 1134'
).put()

maya = User(
	key = ndb.Key(User, 'm.gorzkowicz'),
	username = 'm.gorzkowicz',
	password = 'password',
	photo = 'http://i.imgur.com/TYlbXc0.jpg',
	firstname = 'Maya',
	lastname = 'Gorzkowicz',
	description = 'student',
	email = 'm.gorzkowicz@lancaster.ac.uk',
	phone = '+44 152 4510 387'
).put()

phil = User(
	key = ndb.Key(User, 'p.benachour'),
	username = 'p.benachour',
	password = 'password',
	photo = 'http://i.imgur.com/TYlbXc0.jpg',
	firstname = 'Phil',
	lastname = 'Benachour',
	description = 'lecturer',
	email = 'p.benachour@lancaster.ac.uk',
	phone = '+44 152 4510 387'
).put()

nigel = User(
	key = ndb.Key(User, 'n.davies'),
	username = 'n.davies',
	password = 'password',
	photo = 'http://i.imgur.com/TYlbXc0.jpg',
	firstname = 'Nigel',
	lastname = 'Davies',
	description = 'lecturer',
	email = 'n.davies@lancaster.ac.uk',
	phone = ' +44 (0) 1524 594 337'
).put()