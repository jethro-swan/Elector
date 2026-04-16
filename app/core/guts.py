import datetime, time
import os
import sqlite3
import shutil
from pathlib import Path
import pickle

from app.core.constants import VOTES_LOG
from app.core.constants import VOTERS_DB, MEMBERS_LIST, CANDIDATES_LIST

#==============================================================================

# Return current date+time in "%Y-%m-%d %H:%M (%A)" format
# YYYY-MM-DD hh:mm
def timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#------------------------------------------------------------------------------
# YYYYMMDDhhmmss
def compact_timestamp():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H%M%%S")

#------------------------------------------------------------------------------
# Copy file or directory with metadata and following symlinks:
def fcopysl(src_path, dest_path):
    shutil.copy2(src_path, dest_path, follow_symlinks=True)

#------------------------------------------------------------------------------
# Copy file or directory with metadata but without following symlinks:
def fcopy(src_path, dest_path):
    newpath = shutil.copy2(src_path, dest_path, follow_symlinks=False)
    if newpath == dest_path:
        return(newpath)
    else:
        return("")
    # Returns empty string if unsuccessful

#------------------------------------------------------------------------------
def create_voters_db():

    if os.path.exists(VOTERS_DB):
        fcopy(VOTERS_DB, VOTERS_DB + "_" + compact_timestamp())
        os.remove(VOTERS_DB)

    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        # Create voters table:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS voters (" \
            + "voter_id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, " \
            + "member_email TEXT, " \
            + "voted_already INTEGER DEFAULT 0, " \
            + "vote_count INTEGER DEFAULT 0" \
            + "); "
        )
        voter_id = 0
        with open(MEMBERS_LIST, "r") as ml:
            members = ml.readlines()
            for member_email in members:
                member_email = member_email.strip()
                print(member_email)
                cursor.execute(
                    "INSERT INTO voters " \
                    + "(voter_id, member_email, voted_already, vote_count) " \
                    + "VALUES (?, ?, ?, ?)",
                    (voter_id, member_email, 0, 0)
                )
                voter_id += 1
        conn.commit()
        # Create candidates table:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS candidates (" \
            + "candidate_id INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, " \
            + "candidate_name TEXT" \
            + "); "
        )
        #
        with open(CANDIDATES_LIST, "r") as cl:
            candidates = cl.readlines()
            for candidate_name in candidates:
                candidate_name = candidate_name.strip()
#                print(candidate_name)
                cursor.execute(
                    "INSERT INTO candidates (candidate_name) VALUES (?)",
                    (candidate_name,)
                )
        conn.commit()
        #
        # Create votes table:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS votes (" \
            + "voter_id INTEGER, " \
            + "timestamp TEXT, " \
            + "vote_set BLOB" \
            + "); "
        )
        #
        # Create votes log table:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS votes_log (" \
            + "vote_number INTEGER PRIMARY KEY AUTOINCREMENT DEFAULT 0, " \
            + "timestamp TEXT, " \
            + "voter_id INTEGER, " \
            + "vote_set BLOB" \
            + "); "
        )
        # The votes are recorded as a pickled lists.
        conn.commit()
        cursor.close()


def record_vote(voter_email, vote_set):

    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT voter_id, voted_already, vote_count FROM voters " \
            + "WHERE member_email = ?",
            (voter_email,)
        )
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            return "Voter is not registered"
        voter_id = result[0]    # integer at this point
        voted_already = result[1]   # integer at this point
        vote_count = result[2]  # integer
        #
        # The vote_set is a list containing only "for"|"against"|"abstain" and
        # it is assumed here that it has been constructed correctly.
        if vote_count > 3:
            cursor.close()
            return "Voter has exceeded maximum number of votes"
        if not voted_already:
            voted_already = 1
            cursor.execute(
                "INSERT INTO votes (timestamp, voter_id, vote_set) " \
                + "VALUES (?, ?, ?)",
                (timestamp(), voter_id, pickle.dumps(vote_set))
            )
        else:
            print("Subsequent vote")
            cursor.execute(
                "UPDATE votes " \
                + "SET timestamp = ?, vote_set = ? WHERE voter_id = ?",
                (timestamp(), pickle.dumps(vote_set), voter_id)
            )
        cursor.execute(
            "INSERT INTO votes_log (timestamp, voter_id, vote_set) " \
            + "VALUES (?, ?, ?)",
               (timestamp(), voter_id, pickle.dumps(vote_set))
        )
        vote_count += 1
        cursor.execute(
            "UPDATE voters SET voted_already = ?, vote_count = ? " \
            + "WHERE voter_id = ?",
            (voted_already, vote_count, voter_id)
        )
        conn.commit()
        cursor.close()
        return ""


def prepare_results_csv():

    with sqlite3.connect(VOTERS_DB) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT candidate_id, candidate_name FROM candidates")
        results = cursor.fetchall()
        if results is None:
            print("No candidates listed")
            return ""

        # Get the number of candidates and create a counter for each:
        n_candidates = len(results)
        n_for = [0] * n_candidates
        n_against = [0] * n_candidates
        n_abstain = [0] * n_candidates

        # Create the CSV header row:
        candidates_list = []
        for candidate in results:
            c_num = candidate[0] - 1
            candidates_list.append(candidate[1])

        csvop = "votes,"
        csvop += ",".join(candidates_list)

        cursor.execute("SELECT vote_set FROM votes")
        results = cursor.fetchall()
        cursor.close()

    if results is None:
        print("No votes available")
        return ""

    for result in results:
        # One vote set (row) per voter:
        vote_set = pickle.loads(result[0])
        # One vote per candidate (column) per voter:
        for c in range(n_candidates):
            if vote_set[c] == "for":
                n_for[c] += 1
            elif vote_set[c] == "against":
                    n_against[c] += 1
            else:
                n_abstain[c] += 1

    csvop += "\nfor"
    for c in range(n_candidates):
        csvop += "," + str(n_for[c])
    csvop += "\nagainst"
    for c in range(n_candidates):
        csvop += "," + str(n_against[c])
    csvop += "\nabstain"
    for c in range(n_candidates):
        csvop += "," + str(n_abstain[c])

    print(csvop)
