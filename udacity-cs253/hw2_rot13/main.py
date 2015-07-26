import webapp2
import escape
import rot13

form="""
<form method="post">
    Enter some text to ROT13:
    <br>
    <textarea type="text" name="rotText" value=%(rotText)s>
    </textarea>
    <br>
    
    
    <br>
    <input type="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self, rotText=""):
        self.response.out.write(form % {"rotText" : escape.escape_html(rotText) })  
      
    def get(self):
        self.write_form()
        #self.response.out.write(form)
        
    def post(self):        
        rotTextStr = rot13.rot13(self.request.get('rotText'))
        
        #self.response.out.write(rotTextStr)
        self.write_form(rotTextStr)
        
        
app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
