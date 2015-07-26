#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import validation
import escape

#print Util.escape("<>")
#import escape

form="""
<form method="post">
    What is your birthday?
    <br>
    
    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label>

    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label>
     
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label>
    
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
"""
            
class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error" : error,
                                        "month" : escape.escape_html(month),
                                        "day" : escape.escape_html(day),
                                        "year" : escape.escape_html(year)})  
                
    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        monthIsValid = validation.valid_month(self.request.get('month'))
        dayIsValid = validation.valid_day(self.request.get('day'))
        yearIsValid = validation.valid_year(self.request.get('year'))
        
        if not (monthIsValid and dayIsValid and yearIsValid):
            self.write_form("That does not look valid to me, friend!",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")
            
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!!")


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/thanks', ThanksHandler)],
                              debug=True)


