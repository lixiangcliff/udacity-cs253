import webapp2
import jinja2
import os
import rot13_encode
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
        
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
         
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
     
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(BaseHandler):
    def get(self):
        #logging.info("@@@@in get method@@@@")  
        self.render("rot13-form.html")
        
    def post(self): 
        rot13 = ''
        text = self.request.get('text')  
        if text:
            rot13 = text.encode('rot13') 
            #rot13 = rot13_encode.rot13(self.request.get('text')) @my own method also works.
            #logging.info("@@in post method@@rot13 is 2 @@@%s@@@" % rot13)
        self.render("rot13-form.html", text = rot13)
        
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
