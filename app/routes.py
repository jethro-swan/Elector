#from flask import render_template
from flask import render_template, render_template_string
from flask import flash, redirect, url_for
from flask import session, g, request
from app import app

from app.core.constants import VOTERS_DB
from app.core.constants import MEMBERS_LIST
from app.core.constants import CANDIDATES_LIST
from app.core.constants import VOTES_LOG


@app.route('/read_vote_form', methods=['POST'])
def read_vote_form():

    # Get the form data as Python ImmutableDict datatype
    data = request.form

    email = data['userEmail']
    # INSERT code to check that email is that of a member

    password = data['userPassword']
    if password != "nopasaran":
        flash("Invaid password")
        return redirect(url_for("invalid_password"))

    # INSERT code to store results in database and log

    for k in data.keys():
        print(k + " :: " + data[k])

    flash("Your vote has been recorded")
    return redirect(url_for("vote_recorded"))


@app.route("/vote_recorded")
def vote_recorded():
    return render_template(
        "vote_recorded.html",
        title="vote recorded"
    )

@app.route("/invalid_voter")
def invalid_voter():
    return render_template(
        "invalid_voter.html",
        title="invalid voter"
    )

@app.route("/invalid_password")
def invalid_password():
    return render_template(
        "invalid_password.html",
        title="invalid password"
    )


# vote ------------------------------------------------------------------------
@app.route("/", methods = ["GET"])
@app.route("/vote", methods = ["GET"])
def vote():
    with open(CANDIDATES_LIST, "r") as cl:
        candidates_list = cl.readlines()
    candidates = []
    n_candidates = len(candidates_list)
    for c_num in range(n_candidates):
        candidate = {}
        candidate["id"] = str(c_num)
        candidate["name"] = candidates_list[c_num].strip()
        candidates.append(candidate)

    arg_req = []
    for c_num in range(n_candidates):
        arg_req.append(str(c_num) + "_vote")

    print(candidates)
    for c_num in range(n_candidates):
        arg_req.append(str(c_num) + "_vote")

    return render_template(
        "vote.html",
        title="AGM 2026",
        candidates=candidates
    )
