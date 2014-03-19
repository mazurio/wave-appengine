# Watch later:
# http://stackoverflow.com/questions/11493400/app-engine-no-api-in-explorer

# http://apis-explorer.appspot.com/apis-explorer/?base=http://localhost:10080/_ah/api#p/lancaster/v1/

import webapp2
import endpoints

from Backend import *

application = endpoints.api_server(
	[Backend],
	restricted = False
)

class MainHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('index')

app = webapp2.WSGIApplication([
	webapp2.Route('/', MainHandler)
], debug = True)