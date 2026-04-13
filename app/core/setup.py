import os
import sqlite3
from pathlib import Path


from app.core.constants import VOTERS_DB, MEMBERS_LIST, CANDIDATES_LIST
from app.core.common import compact_timestamp
from app.core.common import fcopy


#==============================================================================
def create_voters_db():

    if os.path.exists(VOTERS_DB):
        fcopy(VOTERS_DB, VOTERS_DB + "_" + compact_timestamp())
        os.remove(VOTERS_DB)

    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS voters (" \
            + "member_email TEXT PRIMARY KEY, " \
            + "login_authenticated INTEGER DEFAULT 0"
            + "); " \
        )

        with open(MEMBERS_LIST, "r") as m:
            members = m.readlines()
            for member_email in members:
                member_email = member_email.strip()
                print(member_email)
                cursor.execute(
                    "INSERT INTO voters (member_email, login_authenticated) "
                    + "VALUES (?, ?)",
                    (member_email, 0)
                )
