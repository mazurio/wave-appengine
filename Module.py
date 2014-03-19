import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

class APIModule(messages.Message):
	id = messages.StringField(1, required = True)
	title = messages.StringField(2, required = True)

class APIModuleList(messages.Message):
	list = messages.MessageField(APIModule, 1, repeated = True)

class Module(ndb.Model):
	id = ndb.StringProperty(required = True)
	title = ndb.StringProperty(required = True)

class ModuleEnrolnment(ndb.Model):
	module = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)

scc300 = Module(
	key = ndb.Key(Module, 'SCC.300'),
	id = 'SCC.300',
	title = 'Final Year Project'
).put()

scc311 = Module(
	key = ndb.Key(Module, 'SCC.311'),
	id = 'SCC.311',
	title = 'Distributed Systems'
).put()

scc300damian = ModuleEnrolnment(
	key = ndb.Key(ModuleEnrolnment, '[d.mazurkiewicz]:[SCC.300]'),
	module = 'SCC.300',
	user = 'd.mazurkiewicz'
).put()

scc311damian = ModuleEnrolnment(
	key = ndb.Key(ModuleEnrolnment, '[d.mazurkiewicz]:[SCC.311]'),
	module = 'SCC.311',
	user = 'd.mazurkiewicz'
).put()

scc300phil = ModuleEnrolnment(
	key = ndb.Key(ModuleEnrolnment, '[p.benachour]:[SCC.300]'),
	module = 'SCC.300',
	user = 'p.benachour'
).put()