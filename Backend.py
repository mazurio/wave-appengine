#
#
# Quality of the code is:
# The number of [Fuck's per minute] * [amount of coffee + amount of energy drinks]
#
#
import logging
import json
import endpoints
import os
import binascii

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from datetime import datetime

from User import *
from Tag import *
from Book import *

from Appointment import *
from Announcement import *

from Module import *
from Device import *

AUTH = endpoints.ResourceContainer(
	message_types.VoidMessage,
	username = messages.StringField(1, required = True),
	password = messages.StringField(2, required = True),
	device = messages.StringField(3, required = True)
)

SYNC = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True)
)

GET_TAG_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True)
)
GET_CONTACT_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True)
)
GET_BOOK_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True),
	timestamp = messages.IntegerField(3, required = True)
)

INSERT_TAG_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True)
)
INSERT_CONTACT_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True)
)
INSERT_BOOK_REQUEST = endpoints.ResourceContainer(
	message_types.VoidMessage,
	auth = messages.StringField(1, required = True),
	id = messages.StringField(2, required = True)
)

INSERT_APPOINTMENT_REQUEST = endpoints.ResourceContainer(
	APIAppointment,
	auth = messages.StringField(1, required = True)
)
CONFIRM_APPOINTMENT_REQUEST = endpoints.ResourceContainer(
	APIAppointment,
	auth = messages.StringField(1, required = True)
)
CANCEL_APPOINTMENT_REQUEST = endpoints.ResourceContainer(
	APIAppointment,
	auth = messages.StringField(1, required = True)
)

INSERT_ANNOUNCEMENT_REQUEST = endpoints.ResourceContainer(
	APIAnnouncement,
	auth = messages.StringField(1, required = True)
)

UPDATE_APPOINTMENT_REQUEST = endpoints.ResourceContainer(message_types.VoidMessage)
UPDATE_ANNOUNCEMENT_REQUEST = endpoints.ResourceContainer(message_types.VoidMessage)

LIST_TAGS_REQUEST = endpoints.ResourceContainer(
	APITagList,
	auth = messages.StringField(1, required = True)
)

LIST_CONTACTS_REQUEST = endpoints.ResourceContainer(
	APIUserList,
	auth = messages.StringField(1, required = True)
)
LIST_BOOKS_REQUEST = endpoints.ResourceContainer(
	APIBookList,
	auth = messages.StringField(1, required = True)
)

LIST_MODULES_REQUEST = endpoints.ResourceContainer(
	APIModuleList,
	auth = messages.StringField(1, required = True)
)

LIST_APPOINTMENTS_REQUEST = endpoints.ResourceContainer(
	APIAppointmentList,
	auth = messages.StringField(1, required = True)
)

LIST_ANNOUNCEMENTS_REQUEST = endpoints.ResourceContainer(
	APIAppointmentList,
	auth = messages.StringField(1, required = True),
	module = messages.StringField(2, required = True)
)

class APISyncList(messages.Message):
	tags = messages.MessageField(APITag, 1, repeated = True)
	contacts = messages.MessageField(APIUser, 2, repeated = True)
	books = messages.MessageField(APIBook, 3, repeated = True)
	modules = messages.MessageField(APIModule, 4, repeated = True)
	announcements = messages.MessageField(APIAnnouncement, 5, repeated = True)
	appointments = messages.MessageField(APIAppointment, 6, repeated = True)

class APIAuthList(messages.Message):
	auth = messages.MessageField(APIUser, 1)
	tags = messages.MessageField(APITag, 2, repeated = True)
	contacts = messages.MessageField(APIUser, 3, repeated = True)
	books = messages.MessageField(APIBook, 4, repeated = True)
	modules = messages.MessageField(APIModule, 5, repeated = True)
	announcements = messages.MessageField(APIAnnouncement, 6, repeated = True)
	appointments = messages.MessageField(APIAppointment, 7, repeated = True)

@endpoints.api(name = 'backend', version = 'v1', description = 'API')
class Backend(remote.Service):
	#
	# Authorize user using username and password credentials.
	#
	@endpoints.method(AUTH, APIAuthList, name = 'auth', path = 'auth', http_method = 'POST')
	def auth(self, request):
		# Check if username is provided.
		if request.username is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Check if password is provided.
		if request.password is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Check if device registration id is provided.
		if request.device is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Check if user exists in the model.
		user = User.get_by_id(request.username)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Check if password does match.
		if user.password != request.password:
			raise endpoints.UnauthorizedException('Invalid password.')

		# Register device with GCM Model.
		device = DeviceSync(
			key = ndb.Key(DeviceSync, request.device),
			device = request.device,
			user = request.username
		)

		# Write:
		device.put()

		# Get the tags that are assigned to this user.
		tag_sync = TagSync.query(TagSync.user == request.username)
		tags = []

		# Append tags with the data that was assigned before or return empty.
		for assignment in tag_sync:
			tag = Tag.get_by_id(assignment.tag)
			tags.append(APITag(
				id = tag.id,
				title = tag.title,
				description = tag.description,
				image = tag.image
			))

		# Get the contacts that are assigned to this user.
		user_sync = UserSync.query(UserSync.user == request.username)
		contacts = []

		# Append contacts with the data that was assigned before or return empty.
		for assignment in user_sync:
			contact = User.get_by_id(assignment.contact)
			contacts.append(APIUser(
				username = contact.username,
				photo = contact.photo,
				firstname = contact.firstname,
				lastname = contact.lastname,
				description = contact.description,
				email = contact.email,
				phone = contact.phone
			))

		# Get the books that are assigned to this user.
		book_sync = BookSync.query(BookSync.user == request.username)
		books = []

		# Append books with the data that was assigned before or return empty.
		for assignment in book_sync:
			book = Book.get_by_id(assignment.book)
			books.append(APIBook(
				id = book.id,
				timestamp = assignment.timestamp,
				title = book.title,
				author = book.author,
				cover = book.cover
			))

		# Get the modules that are assigned to this user.
		enrolnment = ModuleEnrolnment.query(ModuleEnrolnment.user == request.username)
		modules = []
		announcements = []

		# Append modules with the data that was assigned before or return empty.
		for assignment in enrolnment:
			module = Module.get_by_id(assignment.module)
			announcement_query = Announcement.query(Announcement.module == module.id)

			# append announcements for this module
			for announcement in announcement_query:
				announcements.append(APIAnnouncement(
						module = announcement.module,
						user = announcement.user,
						title = announcement.title,
						description = announcement.description,
						timestamp = announcement.timestamp
				))

			# module append
			modules.append(APIModule(
				id = module.id,
				title = module.title
			))

		# Get the appointments that are assigned with this user.
		query = Appointment.query(Appointment.sender == request.username)
		query2 = Appointment.query(Appointment.receiver == request.username)
		
		# List
		appointments = []

		# Append appointments with data.
		for appointment in query:
			appointments.append(APIAppointment(
				timestamp = appointment.timestamp,
				title = appointment.title,
				description = appointment.description,
				status = appointment.status,
				sender = appointment.sender,
				receiver = appointment.receiver,
				date = appointment.date
			))

		# Append appointments with data.
		for appointment in query2:
			appointments.append(APIAppointment(
				timestamp = appointment.timestamp,
				title = appointment.title,
				description = appointment.description,
				status = appointment.status,
				sender = appointment.sender,
				receiver = appointment.receiver,
				date = appointment.date
			))

		# Return the user model.
		return APIAuthList(
			auth = APIUser(
				username = user.username,
				photo = user.photo,
				firstname = user.firstname,
				lastname = user.lastname,
				description = user.description,
				email = user.email,
				phone = user.phone
			),
			tags = tags,
			contacts = contacts,
			books = books,
			modules = modules,
			announcements = announcements,
			appointments = appointments
		)

	#
	# Synchronise the data.
	#
	@endpoints.method(SYNC, APISyncList, name = 'sync', path = 'sync', http_method = 'POST')
	def sync(self, request):
		# Check if user exists in the model.
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Get the tags that are assigned to this user.
		tag_sync = TagSync.query(TagSync.user == request.auth)
		tags = []

		# Append tags with the data that was assigned before or return empty.
		for assignment in tag_sync:
			tag = Tag.get_by_id(assignment.tag)
			tags.append(APITag(
				id = tag.id,
				title = tag.title,
				description = tag.description,
				image = tag.image
			))

		# Get the contacts that are assigned to this user.
		user_sync = UserSync.query(UserSync.user == request.auth)
		contacts = []

		# Append contacts with the data that was assigned before or return empty.
		for assignment in user_sync:
			contact = User.get_by_id(assignment.contact)
			contacts.append(APIUser(
				username = contact.username,
				photo = contact.photo,
				firstname = contact.firstname,
				lastname = contact.lastname,
				description = contact.description,
				email = contact.email,
				phone = contact.phone
			))

		# Get the books that are assigned to this user.
		book_sync = BookSync.query(BookSync.user == request.auth)
		books = []

		# Append books with the data that was assigned before or return empty.
		for assignment in book_sync:
			book = Book.get_by_id(assignment.book)
			books.append(APIBook(
				id = book.id,
				timestamp = assignment.timestamp,
				title = book.title,
				author = book.author,
				cover = book.cover
			))

		# Get the modules that are assigned to this user.
		enrolnment = ModuleEnrolnment.query(ModuleEnrolnment.user == request.auth)
		modules = []
		announcements = []

		# Append modules with the data that was assigned before or return empty.
		for assignment in enrolnment:
			module = Module.get_by_id(assignment.module)
			announcement_query = Announcement.query(Announcement.module == module.id)

			# append announcements for this module
			for announcement in announcement_query:
				announcements.append(APIAnnouncement(
						module = announcement.module,
						user = announcement.user,
						title = announcement.title,
						description = announcement.description,
						timestamp = announcement.timestamp
				))

			# module append
			modules.append(APIModule(
				id = module.id,
				title = module.title
			))

		# Get the appointments that are assigned with this user.
		query = Appointment.query(Appointment.sender == request.auth)
		query2 = Appointment.query(Appointment.receiver == request.auth)
		
		# List
		appointments = []

		# Append appointments with data.
		for appointment in query:
			appointments.append(APIAppointment(
				timestamp = appointment.timestamp,
				title = appointment.title,
				description = appointment.description,
				status = appointment.status,
				sender = appointment.sender,
				receiver = appointment.receiver,
				date = appointment.date
			))

		# Append appointments with data.
		for appointment in query2:
			appointments.append(APIAppointment(
				timestamp = appointment.timestamp,
				title = appointment.title,
				description = appointment.description,
				status = appointment.status,
				sender = appointment.sender,
				receiver = appointment.receiver,
				date = appointment.date
			))

		# Return the user model.
		return APISyncList(
			tags = tags,
			contacts = contacts,
			books = books,
			modules = modules,
			announcements = announcements,
			appointments = appointments
		)

	#
	# Get data about specific tag from the database.
	#
	@endpoints.method(GET_TAG_REQUEST, APITag, name = 'get.tag', path = 'get.tag', http_method = 'GET')
	def get_tag(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Check if tag exists.
		tag = Tag.get_by_id(request.id)
		if tag is None:
			raise endpoints.UnauthorizedException('Invalid id.')

		# Add tag.
		# Create id for UNIQUE key.
		# TODO: This could be done different way using models.
		id = '[' + request.auth + ']:[' + tag.id + ']'

		# Assign this tag with this user.
		sync = TagSync(
			key = ndb.Key(TagSync, id),
			tag = tag.id,
			user = request.auth
		)

		# Write.
		sync.put()

		# Return the tag model.
		return APITag(
			id = tag.id,
			title = tag.title,
			description = tag.description,
			image = tag.image
		)

	#
	# Get data about specific user from the database.
	#
	@endpoints.method(GET_CONTACT_REQUEST, APIUser, name = 'get.contact', path = 'get.contact', http_method = 'GET')
	def get_contact(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Check if user exists.
		user = User.get_by_id(request.id)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid id.')

		# Create id for UNIQUE key.
		# TODO: This could be done different way using models.
		id = '[' + request.auth + ']:[' + request.id + ']'

		# Assign this contact with this user.
		sync = UserSync(
			key = ndb.Key(UserSync, id),
			contact = user.username,
			user = request.auth			
		)

		# Write.
		sync.put()

		# Return the user model.
		return APIUser(
			username = user.username,
			photo = user.photo,
			firstname = user.firstname,
			lastname = user.lastname,
			description = user.description,
			email = user.email,
			phone = user.phone
		)

	#
	# Get data about specific book from the database.
	#
	@endpoints.method(GET_BOOK_REQUEST, APIBook, name = 'get.book', path = 'get.book', http_method = 'GET')
	def get_book(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Check if book exists.
		book = Book.get_by_id(request.id)
		if book is None:
			raise endpoints.UnauthorizedException('Invalid id.')

		# Create id for UNIQUE key.
		# TODO: This could be done different way using models.
		id = '[' + request.auth + ']:[' + request.id + ']'

		sync = BookSync(
			key = ndb.Key(BookSync, id),
			book = book.id,
			user = request.auth,
			timestamp = request.timestamp
		)

		# Write:
		sync.put()

		# Return the book model.
		return APIBook(
			id = book.id,
			timestamp = request.timestamp,
			title = book.title,
			author = book.author,
			cover = book.cover
		)

	#
	# Send appointment request to another user.
	#
	@endpoints.method(INSERT_APPOINTMENT_REQUEST, APIAppointment, name = 'insert.appointment', path = 'insert.appointment', http_method = 'POST')
	def insert_appointment(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Create new appointment:
		appointment = Appointment(
			key = ndb.Key(Appointment, request.timestamp),
			title = request.title,
			description = request.description,
			status = request.status,
			sender = request.sender,
			receiver = request.receiver,
			timestamp = request.timestamp,
			date = request.date
		)

		# Write:
		appointment.put()

		# GCM:
		
		model = DeviceSync.query(DeviceSync.user == request.receiver)
		# Send gcm to every device:
		for device in model:
			# Data which will be send through GCM.
			data = {
				'type' : 'appointment', 
				'timestamp' : request.timestamp, 
				'title' : request.title,
				'description' : request.description,
				'status' : request.status,
				'sender' : request.sender,
				'receiver' : request.receiver,
				'date' : request.date
			}
			# gcm send
			gcm.plaintext_request(registration_id = device.device, data = data)


		# Return the appointment model:
		return APIAppointment(
			timestamp = appointment.timestamp,
			title = appointment.title,
			description = appointment.description,
			status = appointment.status,
			sender = appointment.sender,
			receiver = appointment.receiver,
			date = appointment.date
		)

	#
	# Confirm appointment.
	#
	@endpoints.method(CONFIRM_APPOINTMENT_REQUEST, APIAppointment, name = 'confirm.appointment', path = 'confirm.appointment', http_method = 'POST')
	def confirm_appointment(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Query this appointment:
		query = Appointment.query(Appointment.timestamp == request.timestamp)

		# Update:
		for appointment in query:
			appointment.status = 'CONFIRMED'
			appointment.put()

		gcmsender = DeviceSync.query(DeviceSync.user == request.sender)
		# Send gcm to every device:
		for device in gcmsender:
			# Data which will be send through GCM.
			data = {
				'type' : 'appointment', 
				'timestamp' : request.timestamp, 
				'title' : request.title,
				'description' : request.description,
				'status' : 'CONFIRMED',
				'sender' : request.sender,
				'receiver' : request.receiver,
				'date' : request.date
			}
			# gcm send
			gcm.plaintext_request(registration_id = device.device, data = data)

		gcmreceiver = DeviceSync.query(DeviceSync.user == request.receiver)
		# Send gcm to every device:
		for device in gcmsender:
			# Data which will be send through GCM.
			data = {
				'type' : 'appointment', 
				'timestamp' : request.timestamp, 
				'title' : request.title,
				'description' : request.description,
				'status' : 'CONFIRMED',
				'sender' : request.sender,
				'receiver' : request.receiver,
				'date' : request.date
			}
			# gcm send
			gcm.plaintext_request(registration_id = device.device, data = data)

		# Return the appointment model:
		return APIAppointment(
			timestamp = request.timestamp,
			title = request.title,
			description = request.description,
			status = 'CONFIRMED',
			sender = request.sender,
			receiver = request.receiver,
			date = request.date
		)

	#
	# Cancel Appointment
	#
	@endpoints.method(CANCEL_APPOINTMENT_REQUEST, APIAppointment, name = 'cancel.appointment', path = 'cancel.appointment', http_method = 'POST')
	def cancel_appointment(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')

		# Query this appointment:
		query = Appointment.query(Appointment.timestamp == request.timestamp)

		# Update:
		for appointment in query:
			appointment.status = 'CANCELED'
			appointment.put()

		gcmsender = DeviceSync.query(DeviceSync.user == request.sender)
		# Send gcm to every device:
		for device in gcmsender:
			# Data which will be send through GCM.
			data = {
				'type' : 'appointment', 
				'timestamp' : request.timestamp, 
				'title' : request.title,
				'description' : request.description,
				'status' : 'CANCELED',
				'sender' : request.sender,
				'receiver' : request.receiver,
				'date' : request.date
			}
			# gcm send
			gcm.plaintext_request(registration_id = device.device, data = data)

		gcmreceiver = DeviceSync.query(DeviceSync.user == request.receiver)
		# Send gcm to every device:
		for device in gcmsender:
			# Data which will be send through GCM.
			data = {
				'type' : 'appointment', 
				'timestamp' : request.timestamp, 
				'title' : request.title,
				'description' : request.description,
				'status' : 'CANCELED',
				'sender' : request.sender,
				'receiver' : request.receiver,
				'date' : request.date
			}
			# gcm send
			gcm.plaintext_request(registration_id = device.device, data = data)


		# Return the appointment model:
		return APIAppointment(
			timestamp = request.timestamp,
			title = request.title,
			description = request.description,
			status = 'CANCELED',
			sender = request.sender,
			receiver = request.receiver,
			date = request.date
		)

	#
	# Insert announcement for given module.
	#
	@endpoints.method(INSERT_ANNOUNCEMENT_REQUEST, APIAnnouncement, name = 'insert.announcement', path = 'insert.announcement', http_method = 'POST')
	def insert_announcement(self, request):
		# Check if username is provided.
		if request.auth is None:
			raise endpoints.UnauthorizedException('Not authorized.')

		# Authorize:
		user = User.get_by_id(request.auth)
		if user is None:
			raise endpoints.UnauthorizedException('Invalid user.')


		# Create new announcement:
		announcement = Announcement(
			key = ndb.Key(Announcement, request.timestamp),
			module = request.module,
			user = request.user,
			title = request.title,
			description = request.description,
			timestamp = request.timestamp
		)

		# Write:
		announcement.put()
		logging.warning('announcement.put()')

		# Send GCM to all users enrolled in this module.
		# Get the information about enrolnment for this module.
		query = ModuleEnrolnment.query(ModuleEnrolnment.module == request.module)

		# For every enrolnment in this course:
		for b in query:
			# Get the devices registered for this user.
			model = DeviceSync.query(DeviceSync.user == b.user)
			# Send gcm to every device:
			for device in model:
				# Data which will be send through GCM.
				data = {
					'type' : 'announcement', 
					'module' : request.module, 
					'user' : request.user,
					'title' : request.title,
					'description' : request.description,
					'timestamp' : request.timestamp
				}

				# Send plaintext request if the user sending an announcement is not the same.
				logging.warning('Send plaintext request to other users:' + device.device)
				gcm.plaintext_request(registration_id = device.device, data = data)

		# Return the announcement model:
		return APIAnnouncement(
			module = announcement.module,
			user = announcement.user,
			title = announcement.title,
			description = announcement.description,
			timestamp = announcement.timestamp
		)