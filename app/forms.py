import sys

# Flask components: -----------------------------------------------------------

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import TextAreaField, SelectField, RadioField, HiddenField
from wtforms.validators import DataRequired, InputRequired, Email

#==============================================================================


class VoteForm(FlaskForm):

    email       = StringField(
                    "email address",
                    validators=[DataRequired("required"), Email()]
                  )

    password    = PasswordField(
                    "password",
                    #render_kw={"autocomplete": "on"},
                    validators=[DataRequired("required")]
                  )

    vote        = SubmitField("vote")

#------------------------------------------------------------------------------
