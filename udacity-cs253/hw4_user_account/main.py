import webapp2
import jinja2
import os
import logging
import re
import random
import string
import hashlib
import hmac
from string import letters
from google.appengine.ext import db

secret = 'fart'

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    ###Your code here
    #salt = h.split(',')[1]
    #return h.split(',')[0] == hashlib.sha256(name + pw + salt).hexdigest()
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = "default"):
    return db.Key.from_path('users', group)

def make_secure_val(val):
    return "%s|%s" % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
        
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
         
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
     
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
        
    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', 
                                         "%s=%s; Path=/" % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)
        
    def login(self, user):
        self.set_secure_cookie("user_id", str(user.key().id()))
        pass
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))
    
    
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class User(db.Model):
    username = db.StringProperty(required = True)
    #userid = db.IntegerProperty(required = True) 
    password = db.TextProperty(required = True) # has been hashed
    #salt = db.TextProperty(required = True)
    email = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    
    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())
    
    @classmethod
    def by_name(cls, username):
        u = User.all().filter('username =', username).get()
        return u

    @classmethod
    def register(cls, username, password, email = None):
        pw_hash = make_pw_hash(username, password)
        return User(parent = users_key(), 
                    username = username, 
                    password = pw_hash, 
                    email = email)
    @classmethod    
    def login(cls, username, password):
        u = cls.by_name(username)
        if u and valid_pw(username, password, u.password):
            return u

class Signup(BaseHandler):
    def get(self):
        self.render("signup-form.html")
        
    def post(self): 
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password') 
        verify = self.request.get('verify') 
        email = self.request.get('email') 
        
        params = dict(username = username,
                      email = email)
        
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
        
        
        if User.by_name(username):
            params['error_user_exist'] = "That user already exists!"
            have_error = True 
        
        if have_error:
            self.render("signup-form.html", **params)
        else: 
            u = User.register(username=username, password=password, email=email)
            u.put()
            #self.login(u)
            self.redirect("/welcome?username=" + username)

class UserList(BaseHandler):
    def get(self):
        users = db.GqlQuery("SELECT * FROM User ORDER BY created DESC")
        self.render("userlist.html", users=users)

class Login(BaseHandler):
    def get(self):
        self.render("login-form.html")
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/userlist')
        else:
            errorMsg = 'Invalid login'
            self.render('login-form.html', error = errorMsg)
        
class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.render("userlist.html")
        
class Welcome(BaseHandler):
    def get(self):
        username = self.request.get("username")
        if  valid_username(username):
            self.render("welcome.html", username = username)
        else:
            self.redirect("/signup")
                
app = webapp2.WSGIApplication([('/signup', Signup),
                               ('/userlist', UserList),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/welcome', Welcome)
                               ], debug=True)
