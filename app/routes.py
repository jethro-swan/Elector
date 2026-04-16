#from flask import render_template
from flask import render_template, render_template_string
from flask import flash, redirect, url_for
from flask import session, g, request
from app import app

from app.core.constants import VOTERS_DB
from app.core.constants import MEMBERS_LIST
from app.core.constants import CANDIDATES_LIST
from app.core.constants import VOTES_LOG

from app.core.guts import record_vote

max_votes_per_voter = 3

@app.route("/read_vote_form", methods=["POST"])
def read_vote_form():
    # Convert form data ImmutableDict to a mutable equivalent:
    form_data = request.form.to_dict()
    email = form_data.pop("userEmail")
    password = form_data.pop("userPassword")
    if password != "nopasaran":
        flash("Invaid password")
        return redirect(url_for("invalid_password"))
    vote_set = []
    for k in form_data.keys():
        v = k.split("_")
        n = v[0]
        vote_set.append(form_data[k])
    m = record_vote(email, vote_set)
    print("m = " + m)
    flash(m)
    if not m:
        flash("Your vote has been recorded")
        return redirect(url_for("vote_recorded"))
    elif m == "Voter has exceeded maximum number of votes":
        return redirect(url_for("vote_count_exceeded"))
    else:
        return redirect(url_for("invalid_voter"))

@app.route("/vote_recorded")
def vote_recorded():
    return render_template(
        "vote_recorded.html",
        title="vote recorded"
    )

@app.route("/invalid_voter")
def invalid_voter():
    return render_template(
        "error.html",
        title="invalid voter"
    )

@app.route("/invalid_password")
def invalid_password():
    return render_template(
        "error.html",
        title="invalid password"
    )

@app.route("/vote_count_exceeded")
def vote_count_exceeded():
    return render_template(
        "error.html",
        title="vote count exceeded"
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
    for c_num in range(n_candidates):
        arg_req.append(str(c_num) + "_vote")
    return render_template(
        "vote.html",
        title="AGM 2026",
        max_votes=max_votes_per_voter,
        candidates=candidates
    )
