import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APIBook(messages.Message):
	id = messages.StringField(1, required = True)
	title = messages.StringField(2, required = True)
	author = messages.StringField(3, required = True)
	cover = messages.StringField(4, required = True)
	timestamp = messages.IntegerField(5, required = True)

class APIBookList(messages.Message):
	list = messages.MessageField(APIBook, 1, repeated = True)

class Book(ndb.Model):
	id = ndb.StringProperty(required = True)
	title = ndb.StringProperty(required = True)
	author = ndb.StringProperty(required = True)
	cover = ndb.StringProperty(required = True)

class BookSync(ndb.Model):
	book = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)
	timestamp = ndb.IntegerProperty(required = True)

book1 = Book(
	key = ndb.Key(Book, 'book1'),
	id = 'book1',
	title = 'Programming in Objective-C: Edition 4',
	author = 'Stephen G. Kochan',
	cover = 'http://i.imgur.com/Y1itmfD.jpg'
).put()

book2 = Book(
	key = ndb.Key(Book, 'book2'),
	id = 'book2',
	title = 'A Storm of Swords',
	author = 'George R. R. Martin',
	cover = 'http://i.imgur.com/8VmUcJX.jpg'
).put()

book3 = Book(
	key = ndb.Key(Book, 'book3'),
	id = 'book3',
	title = 'A Game of Thrones: The Story Continues',
	author = 'George R. R. Martin',
	cover = 'http://i.imgur.com/qmwmUV4.jpg'
).put()