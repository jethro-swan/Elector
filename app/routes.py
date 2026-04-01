from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    candidates = {
        "1": "Henry Crun",
        "2": "Dennis Bloodnok",
        "3": "Minnie Bannister"
    }
    return render_template(
        "index.html", title="AGM 2026", candidates=candidates
    )
