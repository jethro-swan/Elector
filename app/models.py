import os
from pathlib import Path
from datetime import datetime
import sys
from itsdangerous import URLSafeTimedSerializer

#from app import app
from app.core.common import unixtime_str, timestamp
from app.core.slate_login import register_authenticated_login
from app.core.slate_login import deregister_authenticated_login
from app.core.slate_login import check_authenticated_login
from app.core.slate_login import get_auth_data
from app.core.auth import check_auth_hash




# Flask components: -----------------------------------------------------------

from flask import Flask, Response
from flask_login import LoginManager, UserMixin

# See
# https://flask-login.readthedocs.io/en/latest/_modules/flask_login/mixins.html

#from app import login_manager


class User(UserMixin):

    def __init__(self, email_address):
        self.id = email_address

    def is_active(self):
        if enabled(self.id) and not pending(self.id):
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return check_authenticated_login(self)

    def mark_authenticated(self):
        register_authenticated_login(self.id)
        return email_address

    def mark_unauthenticated(self):
        deregister_authenticated_login(self.id)
        return ""

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
