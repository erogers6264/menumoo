
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>"
				output += "<form method='POST' enctype='multipart/form-data'\
						   action='/restaurants/new'><h2>What is the new restaurant called?\
						   </h2><input name='message' type='text'><input \
						   type='submit' value='Submit'></form>"

				self.wfile.write(output)
				return


			if self.path.endswith("/restaurants"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>New Restaurant"
				eateries = session.query(Restaurant).all()
				# List comprehensions are useful
				idnames = [(eatery.id, eatery.name) for eatery in eateries]

				for id_number, name in idnames:
					output += "<h2> %s </h2>" % name
					output += "<p><a href='/restaurants/%r/edit'> Edit </a></p>" % id_number
					output += "<p><a href='/delete'> Delete </a></p>"

				output += "<p><a href='/restaurants/new'>Add new restaurant</a></p>"
				output += "</html></body>"
				self.wfile.write(output)
				return

			if self.path.endswith("/hello"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>Hello!"
				output += "<form method='POST' enctype='multipart/form-data'\
						   action='/hello'><h2>What would you like me to say?\
						   </h2><input name='message' type='text'><input \
						   type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				output = ""
				output += "<html><body>&#161Hola! <a href = '/hello'>Back to\
						   Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data'\
						   action='/hello'><h2>What would you like me to say?\
						   </h2><input name='message' type='text'><input \
						   type='submit' value='Submit'></form>"
				output += "</html></body>"

				self.wfile.write(output)
				return 

		except IOError:
			self.send_error(404, "File not found %s" % self.path)

	def do_POST(self):
		try:
			if self.path.endswith('/restaurants/new'):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader(
													'content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				neatery = Restaurant(name = str(messagecontent[0]))
				session.add(neatery)
				session.commit()
				output = ""
				output += "<html><body>"
				output += " <h2> Added new restaurant %s </h2>" % neatery.name
				output += "<form method='POST' enctype='multipart/form-data'\
						   action='/restaurants/new'><h2>What is the new restaurant called?\
						   </h2><input name='message' type='text'><input \
						   type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output)
				return

			if self.path.endswith('/hello'):
				self.send_response(301)
				self.end_headers()

				ctype, pdict = cgi.parse_header(self.headers.getheader(
													'content-type'))
				if ctype == 'multipart/form-data':
					fields=cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('message')

				output = ""
				output += "<html><body>"
				output += " <h2> Okay, how about this: </h2>"
				output += "<h1> %s </h1>" % messagecontent[0]
				output += "<form method='POST' enctype='multipart/form-data'\
							action='/hello'><h2>What would you like me to say?\
							</h2><input name='message' type='text'><input \
							type='submit' value='Submit'></form>"
				output += "</html></body>"
				self.wfile.write(output)
				return

		except Exception:
			pass
		

def main():
	try:
		port = 8080
		server = HTTPServer(('', port), WebServerHandler)
		print "Web Server running on port %s" % port
		server.serve_forever()
	
	except KeyboardInterrupt:
		print "^C entered, stopping web server madness...."
		server.socket.close()

if __name__ == '__main__':
	main()