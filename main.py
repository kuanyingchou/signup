import webapp2
import cgi

form = '''
<form method="post">
  <label>Name
    <input name="username" value="%(username)s">
    <span style="color: red">%(username_error)s</span>
  </label>
  <br>
  <label>Password
    <input name="password" type="password">
    <span style="color: red">%(password_error)s</span>
  </label>
  <br>
  <label>Verify Password
    <input name="verify" type="password">
    <span style="color: red">%(verify_error)s</span>
  </label>
  <br>
  <label>email
    <input name="email" value="%(email)s">
    <span style="color: red">%(email_error)s</span>
  </label>
  <br>
  <input type="submit">
</form>
'''

import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

class MainPage(webapp2.RequestHandler):
    def write_form(self, form, 
            username='', password='', verify='', email='', 
            username_error='', password_error='', verify_error='', email_error=''):
        self.response.write(form % {
            'username':cgi.escape(username),
            'email': cgi.escape(email), 
            'username_error': cgi.escape(username_error),
            'password_error': cgi.escape(password_error),
            'verify_error': cgi.escape(verify_error),
            'email_error': cgi.escape(email_error)
        })

    def get(self):
        self.write_form(form)

    def post(self):
        # self.response.write(self.request)
        # self.response.write('<br>')
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        ok = True;
        username_error=''
        verify_error=''
        password_error=''
        email_error=''

        username_match = USER_RE.match(username)
        if not username_match:
            ok = False
            username_error = 'invalid username'

        password_match = PASSWORD_RE.match(password)
        if not password_match:
            ok = False
            password_error = 'invalid password'

        if password != verify:
            ok = False
            verify_error = "passwords don't match"

        email_match = EMAIL_RE.match(email)
        if email and not email_match:
            ok = False
            email_error = 'email is invalid'

        if not ok: 
            self.write_form(form, username, password, verify, email, 
                    username_error, password_error, verify_error, email_error)
        else:
            self.redirect('/welcome?username=%s' % username)

class WelcomePage(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write("Welcome, %s" % username)

app = webapp2.WSGIApplication([ ('/signup', MainPage), ('/welcome', WelcomePage)], 
        debug=True)
