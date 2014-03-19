import endpoints

from google.appengine.ext import ndb

from protorpc import messages
from protorpc import message_types
from protorpc import remote

from gcm import GCM

gcm = GCM('AIzaSyA2TSvSELSe_DfHakhXujx4MiB14-0jhVg')

CLIENT_ID = '134605304581.apps.googleusercontent.com'
EXPLORER_ID = '292824132082.apps.googleusercontent.com'
CLIENT_ID_ANDROID = '134605304581-v1er84h8bmp6c3pcsmdkgupr716u7jha.apps.googleusercontent.com'

class DeviceSync(ndb.Model):
	device = ndb.StringProperty(required = True)
	user = ndb.StringProperty(required = True)