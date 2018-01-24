from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from flask import Flask, jsonify, render_template, request, session
from sqlalchemy import ForeignKey
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

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
    user = db.Column(db.String(50), ForeignKey("users.user"), primary_key = True)
    bloodForTheBloodGod = db.Column(db.Boolean)
    removePoint = db.Column(db.Boolean)
    def __init__ (self, user, bloodForTheBloodGod, removePoint):
        self.user = user
        self.bloodForTheBloodGod = bloodForTheBloodGod
        self.removePoint = removePoint
