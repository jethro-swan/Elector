import sys

# Flask components: -----------------------------------------------------------

from flask_wtf import FlaskForm, RecaptchaField
#from flask_wtf import Form ###
from wtforms import StringField, PasswordField, BooleanField, SubmitField
#from wtforms import TextField, TextAreaField, SelectField, RadioField
from wtforms import TextAreaField, SelectField, RadioField, HiddenField
from wtforms import IntegerField, DecimalField, FloatField
from wtforms import DateField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, Email
from wtforms.validators import Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed

#==============================================================================






#------------------------------------------------------------------------------

class VoteForm(FlaskForm):

    for candidate in candidates:

        
    category        = RadioField(
                        "Category",
                        choices = [
                                    ("payment_received", "payment received"),
                                    ("offer", "offer"),
                                    ("request", "request"),
                                    ("payment_request", "payment request"),
                                    ("event", "event"),
                                    ("other", "other")
                                  ],
                        default = "other"
                      )


    vote    = SubmitField("vote")

#------------------------------------------------------------------------------

class LoginForm(FlaskForm):

    email           = StringField("email address")

    submit          = SubmitField("log in")

#------------------------------------------------------------------------------
