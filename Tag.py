import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APITag(messages.Message):
	id = messages.StringField(1, required = True)
	title = messages.StringField(2, required = True)
	description = messages.StringField(3, required = True)
	image = messages.StringField(4, required = True)

class APITagList(messages.Message):
	list = messages.MessageField(APITag, 1, repeated = True)

class Tag(ndb.Model):
	id = ndb.StringProperty(required = True)
	title = ndb.TextProperty(required = True)
	description = ndb.TextProperty(required = True)
	image = ndb.StringProperty(required = True)

class TagSync(ndb.Model):
	tag = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)

bowland = Tag(
	key = ndb.Key(Tag, 'infolab21'),
	id = 'infolab21',
	title = 'InfoLab 21',
	description = 'Since opening in 2005 InfoLab21 at Lancaster University has built up a strong reputation as an international Centre of Excellence for research in information and communication technologies and for supporting regional businesses through networking events, workshops and funded ICT programmes.',
	image = 'http://farm8.staticflickr.com/7326/10821485826_b26f72ed9a_h.jpg'
).put()

sports_centre = Tag(
	key = ndb.Key(Tag, 'sports'),
	id = 'sports',
	title = 'Sports Centre',
	description = 'The Sports Centre has workout classes to suit everyone!',
	image = 'http://farm9.staticflickr.com/8452/8062085046_57fd6b3f2a_h.jpg'
).put()

university = Tag(
	key = ndb.Key(Tag, 'university'),
	id = 'university',
	title = 'Lancaster University',
	description = 'Consistently rated as one of the top 10 UK universities, Lancaster University has established an excellent track record in its "Third Mission" activities, which aim to bring universities, businesses and communities together. The University has particular strengths in ICT and has a long and successful history of working with international ICT companies through its prestigious Computing Department and Department Communication Systems, including collaboration with major telecommunications network operators, equipment manufacturers and software providers such as Microsoft, BT Labs, Orange, Cisco, Nokia and Ford.',
	image = 'http://farm7.staticflickr.com/6065/6082178970_1eef7b85bd_b.jpg'
).put()

roses = Tag(
	key = ndb.Key(Tag, 'roses2014'),
	id = 'roses2014',
	title = 'Roses 2014',
	description = 'ROSES 2014 will be taking place on Friday 2nd May, Saturday 3rd May and Sunday 4th May in Lancaster and to add that extra excitement to the tournament it coincides with the 50th anniversary of the University of Lancaster and the 50th year that the event has taken place.',
	image = 'http://farm8.staticflickr.com/7183/6998586248_aea9944151_h.jpg'
).put()

arts = Tag(
	key = ndb.Key(Tag, 'arts'),
	id = 'arts',
	title = 'Faculty of Arts and Scienses',
	description = 'FASS is a research intensive Faculty at one of the UKs leading research Universities. At FASS we are rightly proud of the high quality teaching and research that we deliver. Across a range of disciplines in the Arts, Social Sciences and Humanities, FASS provides outstanding undergraduate and postgraduate training.',
	image = 'http://farm6.staticflickr.com/5010/5280003062_e2ab41e124_b.jpg'
).put()