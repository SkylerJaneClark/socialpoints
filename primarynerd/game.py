from . import pythonConfig

equalExchangeValue = 5




def start(user, users_affected, ability_used ):
    if((user == "" or user == None) or (users_affected==[] or users_affected == None) or (ability_used == [] or ability_used == None)): 
        return (json.dumps({"result":"inputs not filled"}))
    
    elif (str(ability_used) == "equalExchange"):
        return(equalExchange(user, users_affected, ability_used))
    else:
        return json.dumps({"result":"oh god that's my bad, that button don't work"})




def equalExchange(user, users_affected, ability_used):
    fuckery_data = {}
    fuckery_data["result"]="success"

    for person in users_affected:
        victim_points = fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=person).first().points 
        user_points = fuckeries.query.order_by(fuckeries.time.desc()).filter_by(victim=user).first().points
            
        actor_data = users.query.filter_by(user=user).first().user
        victim_data = users.query.filter_by(user=person).first().user
        victim_points_data = victim_points - equalExchangeValue
        user_points_data = user_points -equalExchangeValue
        time_data = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        fuckery_data[actor_data] = user_points_data
        fuckery_data[victim_data] = victim_points_data  

        if user_points_data <= 0:
            return json.dumps({"result": "you don't have enough points to pay for this action"})

        if actor_data == victim_data:
            user_points_data -= equalExchangeValue
            fuckery_data[victim_data] = user_points_data
            fuckery_data[actor_data] = user_points_data
            cost = fuckeries(victim=actor_data, actor=victim_data, points=user_points_data, time=time_data)
            db.session.add(cost)
            db.session.flush()
            db.session.commit()
            return json.dumps(fuckery_data)
    
        cost = fuckeries(victim=actor_data, actor=victim_data, points=user_points_data, time=time_data)
        attack = fuckeries(victim=victim_data, actor=actor_data, points=victim_points_data, time=time_data)
       
        db.session.add(cost)
        db.session.add(attack)
        db.session.flush()
        db.session.commit()
        return json.dumps(fuckery_data)
