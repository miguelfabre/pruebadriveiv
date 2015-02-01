# -*- coding: utf-8 -*-
import cgi
import webapp2
import time
import httplib2
import jinja2
import os
import urllib
#import gflags
import gdata.spreadsheet.service
import gspread
import json
 
from pprint import pprint 

from google.appengine.api import users

from apiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.tools import run

from google.appengine.api import memcache
from oauth2client.appengine import AppAssertionCredentials


#from google.appengine.ext import webapp
from oauth2client.appengine import OAuth2Decorator

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(45)


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

class MainPage(webapp2.RequestHandler):
    def get(self):
		gc = gspread.login(email, password)
		sht1 = gc.open_by_key(spreadsheet_key)
		worksheet = sht1.get_worksheet(0)
		matriz = []
		num_cols = worksheet.col_count
		num_fils = worksheet.row_count
		#Metemos un bucle que recorra toda la hoja y vamos almacenando los datos en una matriz (array de array)
		i = 1
		j = 1
		while i < num_fils:
			matriz.append([])
			while j <= num_cols:
		#Recorremos el documento de forma inversa para mostrar en el blog primero los eventos mas actuales (insertados los ultimos en la hoja de calculo
				val = worksheet.cell(num_fils-i+1, j).value
				matriz[i-1].append(val)
				j = j + 1
			i = i + 1
			j = 1
		
		# Ahora devolvemos la matriz al html, donde con js la cogeremos y la iremos formateando para mostrar los eventos en el blog
		template_values = {'matriz': matriz, 'num_fils': num_fils, 'num_cols': num_cols}
		template = JINJA_ENVIRONMENT.get_template('templates/MAIN_PAGE_HTML_BOOT.html')
		self.response.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
   @decorator.oauth_required
   def post(self):
	client = gdata.spreadsheet.service.SpreadsheetsService()
	client.debug = True
	client.email = email
	client.password = password
	client.source = 'test client'
	client.ProgrammaticLogin()

	if self.request.get('inscripcion') == "inscripcion_si":
		inscripcion = "Si"
	else:
		inscripcion = "No"

	if self.request.get('diploma') == "diploma_si":
		diploma = "Si"
	else:
		diploma = "No"

	if self.request.get('tipo') == "tipo_osl":
		tipo = "OSL"
	elif self.request.get('tipo') == "tipo_compratido":
		tipo = "tipo_compratido"
	else:
		tipo = "tipo_fuera"
	    
	rows = []
	tiempo = time.strftime("%c")
	rows.append({'titulo':cgi.escape(self.request.get('InputName')),'ponente':cgi.escape(self.request.get('InputPonente')),'fecha':tiempo,'inscripcion':inscripcion,'diploma':diploma,'tipo':tipo,'descripcion':cgi.escape(self.request.get('InputDescripcion')),'dia':cgi.escape(self.request.get('dia')),'mes':cgi.escape(self.request.get('mes')),'anio':cgi.escape(self.request.get('anio')),'hora':cgi.escape(self.request.get('hora')),'minuto':cgi.escape(self.request.get('minuto'))})
	for row in rows:
		try:
			client.InsertRow(row, spreadsheet_key, worksheet_id)
		except Exception as e:
			print e
	
	fecha_evento = ""+self.request.get('anio')+"-"+self.request.get('mes')+"-"+self.request.get('dia')

	http = decorator.http()
	event = {"end": {"date": fecha_evento},"start": {"date": fecha_evento},"summary": cgi.escape(self.request.get('InputName')),"description": cgi.escape(self.request.get('InputDescripcion'))}
	request = service.events().insert(calendarId='proyectoivosl@gmail.com', body=event).execute(http=http)
	
	template_values = {}
	template = JINJA_ENVIRONMENT.get_template('templates/hoja_calculo.html')
	self.response.write(template.render(template_values))

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
	rows.append({'id':'Prueba','title':'tiempo'})
	for row in rows:
		try:
			client.InsertRow(row, spreadsheet_key, worksheet_id)
			print "Se ha insertado con exito"
			print "id = Prueba"
			print "title = "+tiempo
		except ValueError:
		    print "No se ha podido insertar"

	self.response.write(URL_SPREADSHEET_HTML)

class Formulario(webapp2.RequestHandler):
    def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('templates/formulario.html')
		self.response.write(template.render(template_values))

class Hoja(webapp2.RequestHandler):
    def get(self):
		template_values = {}
		template = JINJA_ENVIRONMENT.get_template('templates/hoja_calculo.html')
		self.response.write(template.render(template_values))

class Certificado(webapp2.RequestHandler):
    def post(self):
		ponente = self.request.get('InputPonente')
		evento = self.request.get('InputName')
		dia = self.request.get('dia')
		mes = self.request.get('mes')
		anio = self.request.get('anio')
		hora = self.request.get('hora')
		minuto = self.request.get('minuto')
		descripcion = self.request.get('InputDescripcion')
		#ponente = "Manolo"
		#evento = "Evento"
		#dia = "Diass"
		#mes = "Messs"
		#anio = "Anioss"
		#hora = "Horasss"
		#minuto = "Minutosss"
		template_values = {'ponente': ponente, 'evento': evento, 'dia': dia, 'mes': mes, 'anio': anio, 'hora': hora, 'minuto': minuto, 'descripcion': descripcion}
		template = JINJA_ENVIRONMENT.get_template('templates/certificado.html')
		self.response.write(template.render(template_values))

class Json_inserta(webapp2.RequestHandler):
    def get(self):
		gc = gspread.login(email, password)
		sht1 = gc.open_by_key(spreadsheet_key)
		worksheet = sht1.get_worksheet(0)
		val = worksheet.cell(4, 1).value
		val1 = worksheet.row_count
		self.response.write(val1)
		

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook),
	('/formulario', Formulario),
	('/hoja', Hoja),
	('/certificado', Certificado),
    ('/test', test),
	('/inserta', MainHandler),	
	('/json', Json_inserta),
	(decorator.callback_path, decorator.callback_handler())

], debug=True)

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True)


# ---------------------------------------------

