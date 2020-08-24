from flask import Flask
from flask import jsonify
from flask import request
from database import Database
from datetime import datetime

app = Flask(__name__)

db = Database()

@app.route('/api/activities')
def activities():
    start_time = request.args.get("start_time")
    if start_time == None:
        start_time = 0
    end_time = request.args.get("end_time")
    if end_time == None:
        end_time = int(datetime.now().timestamp())

    activities = db.get_activities(start_time, end_time)
    responce = jsonify(activities)
    responce.headers.add('Access-Control-Allow-Origin', '*')
    return responce

if __name__ == '__main__':
    app.run(host='0.0.0.0')
