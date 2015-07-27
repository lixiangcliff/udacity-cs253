import webapp2
import jinja2
import os
import logging
import re

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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(BaseHandler):
    def get(self):
        #logging.info("@@@@in get method@@@@")  
        self.render("signup-form.html")
        
    def post(self): 
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password') 
        verify = self.request.get('verify') 
        email = self.request.get('email') 
        
        #message to store and pass 
        params = dict(username = username,
                      email = email)
          
        #logging.info("@@in post method@@rot13 is 2 @@@%s@@@" % rot13)
        
        if not valid_username(username):
            params['error_username'] = "That is not a valid username!"
            have_error = True
            
        if not valid_password(password):
            params['error_password'] = "That is not a valid password!"
            have_error = True
        elif password != verify:
            params['error_verify'] = "Passwords do not match!"
            have_error = True            
                      
        if not valid_email(email):
            params['error_email'] = "That is not a valid email!"
            have_error = True            
        
        if have_error:
            self.render("signup-form.html", **params)
        else: 
            #Do not render welcome.html here! 
            #instead transfer the necessary data to Welcome class, let it to render
            self.redirect("/welcome?username=" + username)
        
class Welcome(BaseHandler):
    def get(self):
        username = self.request.get("username")
        if  valid_username(username):
            self.render("welcome.html", username = username)
        else:
            self.redirect("/signup")
                
app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/welcome', Welcome)
                               ], debug=True)
