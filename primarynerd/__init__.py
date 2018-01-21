from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask import Flask, render_template, request, session
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from sqlalchemy import ForeignKey
from datetime import datetime

import os

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

auth = OIDCAuthentication(app,
                          issuer=app.config['OIDC_ISSUER'],
                          client_registration_info=app.config['OIDC_CLIENT_CONFIG'])
db = SQLAlchemy(app)

class fuckeries(db.Model):
    victim = db.Column(db.Integer, ForeignKey("users.user"), primary_key = True)
    actor = db.Column(db.Integer, ForeignKey("users.user"), primary_key = True)
    points = db.Column(db.Integer)
    time = db.Column(db.DateTime, primary_key = True)
    def __init__ (self, victim, actor, points, time):
        self.victim = victim
        self.actor = actor
        self.points = points
        self.time = time
    

class users(db.Model):
    user = db.Column(db.Text, primary_key = True)
    emojis = db.Column(db.Text)
    def __init__ (self, user, emojis):
        self.user = user
        self.emojis = emojis

def get_metadata():
    uuid = str(session["userinfo"].get("sub", ""))
    uid = str(session["userinfo"].get("preferred_username", ""))
    metadata = {
        "uuid": uuid,
        "uid": uid,
    }
    return metadata


@app.route("/")
@auth.oidc_auth
def hello():
    db.create_all()
    user_list = []
    for user in users.query.all():
        user_list.append(fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=user.user).first())
    metadata = get_metadata()
    return render_template("index.html", metadata=metadata, user_list=user_list)

@app.route('/logout')
@auth.oidc_logout
def logout():
    return redirect(url_for('hello'), 302)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
