from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask import Flask, jsonify, render_template, request, session
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
import json
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
    victim = db.Column(db.String(50), ForeignKey("users.user"), primary_key = True)
    actor = db.Column(db.String(50), ForeignKey("users.user"), primary_key = True)
    points = db.Column(db.Integer)
    time = db.Column(db.DateTime, primary_key = True)
    def __init__ (self, victim, actor, points, time):
        self.victim = victim
        self.actor = actor
        self.points = points
        self.time = time
        

class users(db.Model):
    user = db.Column(db.String(50), primary_key = True)
    emojis = db.Column(db.String(2000))
    timeDelay = db.Column(db.Integer)
    pointsPerClick = db.Column(db.Integer)
    def __init__ (self, user, emojis, timeDelay, pointsPerClick):
        self.user = user
        self.emojis = emojis
        self.timeDelay = timeDelay
        self.pointsPerClick = pointsPerClick

class abilities(db.Model):
    user = db.Column(db.String(50),primary_key = True)
    bloodForTheBloodGod = db.Column(db.Boolean)
    removePoint = db.Column(db.Boolean)
    def __init__ (self, user, bloodForTheBloodGod, removePoint):
        self.user = user
        self.bloodForTheBloodGod = bloodForTheBloodGod
        self.removePoint = removePoint
        
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
    abilities_dict = {}
    metadata = get_metadata()  
    #currentUser = get_metadata()["uid"]
    currentUser = "god"
    #TODO: set this to organize by most recent fuckery for each user.
    for user in users.query.all():
        user_list.append(fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=user.user).first())
    ability = abilities.query.filter_by(user=currentUser)[0]    
    abilities_dict = dict((col, getattr(ability, col)) for col in ability.__table__.columns.keys())
    abilities_list = [key for key,val in abilities_dict.items() if val==True]
    
    return render_template("index.html", metadata=metadata, user_list=user_list, abilities_list = abilities_list )

@app.route('/logout')
@auth.oidc_logout
def logout():
    return redirect(url_for('hello'), 302)


@app.route('/send_attack', methods = ['PUT'])
def send_attack():
    data = json.loads(request.data.decode('utf-8'))
    #currentuser = get_metadata()["uid"]
    currentuser = "god"
    users_affected = data['users_affected']
    ability_used = data['ability_used']
    return json.dumps({
        "shit":"shit"
        })

@app.route('/add_points', methods = ['PUT'])
def add_points():
    data = json.loads(request.data.decode('utf-8'))
    #TODO: remove god and set currentuser as the actual user 
    #currentuser = get_metadata()["uid"]
    currentuser = "god"
    dbUser = users.query.filter_by(user=currentuser).first()
    currentTime = (datetime.fromtimestamp(float(data['time'])/1000.0))
    relevantFuckery =fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=currentuser).first() 
    lastEvent = relevantFuckery.time
    nextEvent = lastEvent + timedelta(seconds=dbUser.timeDelay)
    points = dbUser.pointsPerClick
    lastPoints = relevantFuckery.points

    if nextEvent < currentTime:
        victim_data = currentuser
        actor_data = "god"
        time_data = currentTime
        points_data = points + lastPoints
        fuckery = fuckeries (victim=victim_data, time=time_data, actor=actor_data, points=points_data)
        db.session.add(fuckery)
        db.session.flush()
        db.session.commit()
        return json.dumps({'cooldown':'inactive',
                           'currentpoints':points_data,
                           'cooldowntime':dbUser.timeDelay})
    else:
        
        return json.dumps({'cooldown':'active',
                           'currentpoints':points_data,
                           'cooldowntime':dbUser.timeDelay})
if __name__ == "__main__":
    app.run(host='0.0.0.0')
