'''
Created on Jul 28, 2015

@author: clli
'''
import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    #even error happens, content will still be reserved
    def render_front(self, subject="", blog="", error=""):
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC ")
        #attention to the value for blog
        self.render("main.html", subject=subject, blog=blog, error=error, blogs=blogs)
    
    def get(self):
        self.render_front()
        
    def post(self):
        pass
            
class NewPost(Handler):
    def render_front(self, subject="", blog="", error=""):
        #attention to the value for blog
        self.render("newpost.html", subject=subject, blog=blog, error=error)
    
    def get(self):
        self.render_front()
        
    def post(self):   
        subject = self.request.get("subject")
        blog = self.request.get("blog")
        
        if subject and blog:
            #self.write("Thanks!")
            b = Blog(subject = subject, blog = blog)
            b.put()
            
            self.redirect("/")
        else:
            error = "We need both a subject and a blog article!"
            self.render_front(subject, blog, error)        

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/newpost', NewPost)], debug=True)