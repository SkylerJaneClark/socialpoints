from pythonConfig import *

removePointsValue = 20

def start(user, users_affected, ability_used ):
    if((user == "" or user == None) or (users_affected==[] or users_affected == None) or (ability_used == [] or ability_used == None)):
        
        return (json.dumps({"result":"inputs not filled"}))
   
    elif (str(ability_used == "removePoints")):
        return(removePoints(user, users_affected, ability_used))

def removePoints(user, users_affected, ability_used):
    for person in users_affected:
        last_points = fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=person).first().points 
        
        actor_data = users.query.filter_by(user=user).first().user
        victim_data = users.query.filter_by(user=person).first().user
        points_data = last_points - removePointsValue
        time_data = (datetime.now().time()).strftime('%Y-%m-%d %H:%M:%S')
        fuckery = fuckeries(victim=victim_data, time=time_data, actor=actor_data, points=points_data)
        
        db.session.add(fuckery)
        db.session.flush()
        db.session.commit()
        
        return json.dumps({"result":"oh jesus christ it worked"})

    return("nani")


