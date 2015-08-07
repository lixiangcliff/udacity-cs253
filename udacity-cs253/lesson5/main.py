'''
Created on Jul 28, 2015

@author: clli
'''
import os
import webapp2
import jinja2
import urllib2
from xml.dom import minidom 
from google.appengine.ext import db
from urllib2 import URLError

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    ip = "24.6.31.146" #sgx
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty(required = True)

class MainPage(BlogHandler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC ")
        #attention to the value for art
        self.render("front.html", title=title, art=art, error=error, arts=arts)
    
    def get(self):
        #self.write(get_coords(self.request.remote_addr))
        self.write(repr(get_coords(self.request.remote_addr)))
        self.render_front()
        
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if art and title:
            #self.write("Thanks!")
            a = Art(title = title, art = art)
            #make map
            coords = get_coords(self.request.remote_addr)
            if a.coords:
                a.coords = coords
            a.put()
            
            self.redirect("/")
        else:
            error = "We need both a title and an artwork!"
            self.render_front(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)