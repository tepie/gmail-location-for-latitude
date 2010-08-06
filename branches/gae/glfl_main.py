#from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
#from google.appengine.ext import db

#import cgi,os,logging,sys

#class Preferences(db.Model):
#	who = db.UserPropery(required=True)
#	latitude_token = db.StringProperty(required=True)
#	gmail_token = db.StringProperty(required=True)
#	trusted_from = db.StringProperty(required=False)
#	created = db.DateTimeProperty(auto_now_add=True)
#	updated = db.DateTimeProperty(auto_now=True)

class MainPage(webapp.RequestHandler):
	def get(self):
		pass
		#user_preferences_query = db.GqlQuery("SELECT * FROM Preferences WHERE owner = :1", users.get_current_user())
		#results = user_preferences_query.fetch(1)
		
		#preference_model = None
		
		#if len(ressults) == 1: for result in results: preference_model = result
		
		#_template_values = {'preferences' : preference_model}
		
		#_path = os.path.join(os.path.dirname(__file__), 'Template_MainPage.html')
		#self.response.out.write(template.render(_path, _template_values))

application = webapp.WSGIApplication([('/', MainPage)],debug=True)

def main():
	run_wsgi_app(application)

if __name__ == "__main__":
	main()