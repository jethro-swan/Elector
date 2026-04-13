import sqlite3
#import random
import os
#import pickle
#from pathlib import Path

from app.core.constants import VOTERS_DB






#==============================================================================

def member_exists(voter_email):
    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM voters WHERE member_email = ?",
            (voter_email,)
        )
        result = cursor.fetchone()
        if not (result is None):
            return True
        else:
            return False

#------------------------------------------------------------------------------

def set_login_authentication_state(voter_email, state):
    if not member_exists(voter_email):
        return False
    if not (state in [True, False, 1, 0]):
        return False
    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE voters SET login_authenticated = ? WHERE member_email = ?",
            (int(state), voter_email)
        )
        conn.commit()
        cursor.close()
    return True

def register_authenticated_login(voter_email):
    return set_login_authentication_state(voter_email, True)

def deregister_authenticated_login(voter_email):
    return set_login_authentication_state(voter_email, False)

def check_authenticated_login(voter_email):
    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT login_authenticated FROM voters WHERE member_email = ?",
            (voter_email,)
        )
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False
        elif result[0] == 1:
            return True
        else:
            return False



#------------------------------------------------------------------------------
