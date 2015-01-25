# -*- coding: utf-8 -*-
#Importación de bibliotecas
import cgi
import webapp2
import time

import gdata.spreadsheet.service
from google.appengine.api import users

#Conexión para crear/modificar la hoja de cálculo en drive
email = 'proyectoivosl@gmail.com'
password = 'pakhires'
spreadsheet_key = '1R3zLvtKxllRM71PdCDQu9XhNYo7xmf0On49WreyLi24' # key param
worksheet_id = 'od6' # default

#Formulario HTML

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
	<h3>Nombre del evento</h3>
      <div><textarea name="nombre" rows="3" cols="60"></textarea></div>
	<h3>Descripcion del evento</h3>
      <div><textarea name="descripcion" rows="3" cols="60"></textarea></div>
      <div><input type="submit" value="Enviar datos"></div>
    </form>
  </body>
</html>
"""

#URL de la hoja de cálculo
URL_SPREADSHEET_HTML = """\
<html>
  <body>
    <a href="https://docs.google.com/spreadsheets/d/1R3zLvtKxllRM71PdCDQu9XhNYo7xmf0On49WreyLi24/edit#gid=0">Enlace a la hoja de calculo de Google Drive</a>
    </form>
  </body>
</html>
"""

#Manejador del formulario
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)

#Manejador que lee los datos del formulario y realiza la inserción
class Guestbook(webapp2.RequestHandler):
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
		self.response.write(URL_SPREADSHEET_HTML)

#Manejador para ejecutar el test	    
class Test(webapp2.RequestHandler):
	def get(self):
		self.response.write(URL_SPREADSHEET_HTML)

	def Inserta(self,valor):
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
			except ValueError:
				print "No se ha podido insertar"
				valor = "error"
		
		return valor

#Manejador de enlaces
application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
    ('/test', Test)
], debug=True)


# ---------------------------------------------

