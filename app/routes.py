#from flask import render_template
from flask import render_template, render_template_string
from flask import flash, redirect, url_for
from flask import session, g, request
#from flask import Flask, session, g, request
#from flask_mailman import Mail, EmailMessage
#from flask_mailman import EmailMessage
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_login import login_required
from flask import send_file
#from flask import send_from_directory
from app import app

# log in to vote --------------------------------------------------------------
@app.route("/", methods = ["GET", "POST"])
@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated: # user is already logged in
        return redirect(url_for("vote"))
    form = LoginForm()
    if form.validate_on_submit():
        password = form.password.data
        if password == "nopasaran":
            return redirect(url_for("vote"))
    return render_template(
        "login.html",
        title = "Sign in",
        form = form
    )


# log out ---------------------------------------------------------------------
@app.route("/logout")
@login_required
def logout():
    user = current_user.get_id()
    logout_user() # a Flask function
    return redirect(url_for("login"))

# vote ------------------------------------------------------------------------
@app.route("/vote")
@login_required
def vote():
    candidates = []
    with open("/var/elector/candidates.txt", "r") as cl:
        candidates = cl.readlines()
    # TESTSTUFF
    for c in candidates:
        print(c)
    ###########
    if form.validate_on_submit():
        print("ZZZZZ")



    return render_template(
        "vote.html",
        title="AGM 2026",
        candidates=candidates
    )
