import cgi
import webapp2
import time
import httplib2
#import gflags
import gdata.spreadsheet.service

from google.appengine.api import users

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials


#from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator


#FLAGS = gflags.FLAGS

email = 'proyectoivosl@gmail.com'
password = 'pakhires'
spreadsheet_key = '1R3zLvtKxllRM71PdCDQu9XhNYo7xmf0On49WreyLi24' # key param
worksheet_id = 'od6' # default

decorator = OAuth2Decorator(
  client_id='97297373612-mvc0t7e42nblkricfi4sn6tfcqqptjo2.apps.googleusercontent.com',
  client_secret='qbtiG-fyhN9iTucuu8OBdC98',
  scope='https://www.googleapis.com/auth/calendar')

service = build('calendar', 'v3', developerKey='AIzaSyDwEDO-Qa3ep2l6kP2e_r6ivjKF28D6LXk')

class MainHandler(webapp2.RequestHandler):
  @decorator.oauth_required
  def get(self):
    # Get the authorized Http object created by the decorator.
	http = decorator.http()
    #credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/devstorage.read_write')
    #http = credentials.authorize(httplib2.Http(memcache))
    # Call the service using the authorized Http object.
	event = {"end": {"date": "2015-01-14"},"start": {"date": "2015-01-14"},"description": "Prueba"}
	request = service.events().insert(calendarId='pacops32@gmail.com', body=event).execute(http=http)
	#response = request.execute(http=http)

#created_event = service.events().insert(calendarId='pacops32@gmail.com', body=event).execute(http=http)

#print created_event['id']



# If the Credentials don't exist or are invalid, run through the native client
# flow. The Storage object will ensure that if successful the good
# Credentials will get written back to a file.
#storage = Storage('calendar.dat')
#credentials = storage.get()
#if credentials is None or credentials.invalid == True:
 # credentials = run(FLOW, storage)

# Create an httplib2.Http object to handle our HTTP requests and authorize it
# with our good Credentials.
#http = httplib2.Http()
#http = credentials.authorize(http)

# Build a service object for interacting with the API. Visit
# the Google Developers Console
# to get a developerKey for your own application.
#service = build(serviceName='calendar', version='v3', http=http,
 #      developerKey='AIzaSyB1dvOxqEYS8KzIZZZT4ez1eMl4b3SGlDU')



MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
	<h3>Nombre del evento</h3>
      <div><textarea name="nombre" rows="3" cols="60"></textarea></div>
	<h3>Descripcion del evento</h3>
      <div><textarea name="descripcion" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Enviar datos"></div>

		<iframe src="https://www.google.com/calendar/embed?src=proyectoivosl%40gmail.com&ctz=Europe/Madrid" style="border: 0" width="400" height="200" frameborder="0" scrolling="no"></iframe>
    </form>
  </body>
</html>
"""

URL_SPREADSHEET_HTML = """\
<html>
  <body>
    <a href="https://docs.google.com/spreadsheets/d/1R3zLvtKxllRM71PdCDQu9XhNYo7xmf0On49WreyLi24/edit#gid=0">Enlace a la hoja de calculo de Google Drive</a>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)	

class Guestbook(webapp2.RequestHandler):
   @decorator.oauth_required
   def post(self):
	client = gdata.spreadsheet.service.SpreadsheetsService()
	client.debug = True
	client.email = email
	client.password = password
	client.source = 'test client'
	client.ProgrammaticLogin()
	    
	rows = []
	rows.append({'id':cgi.escape(self.request.get('nombre')),'title':cgi.escape(self.request.get('descripcion'))})
	#rows.append({'id':'123','title':'12313'})	    
	for row in rows:
		try:
			client.InsertRow(row, spreadsheet_key, worksheet_id)
		except Exception as e:
			print e
	#return
	

	http = decorator.http()
	event = {"end": {"date": "2015-01-12"},"start": {"date": "2015-01-12"},"description": cgi.escape(self.request.get('descripcion'))}
	request = service.events().insert(calendarId='proyectoivosl@gmail.com', body=event).execute(http=http)

	self.response.write(URL_SPREADSHEET_HTML)

class test(webapp2.RequestHandler):
   def get(self):
	client = gdata.spreadsheet.service.SpreadsheetsService()
	client.debug = True
	client.email = email
	client.password = password
	client.source = 'test client'
	client.ProgrammaticLogin()
	rows = []
	tiempo = time.strftime("%c")
	rows.append({'id':'Prueba','title':tiempo})
	for row in rows:
		try:
			client.InsertRow(row, spreadsheet_key, worksheet_id)
			print "Se ha insertado con exito"
			print "id = Prueba"
			print "title = "+tiempo
		except ValueError:
		    print "No se ha podido insertar"

	self.response.write(URL_SPREADSHEET_HTML)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/test', test),
	('/inserta', MainHandler),
	(decorator.callback_path, decorator.callback_handler())

], debug=True)


# ---------------------------------------------

