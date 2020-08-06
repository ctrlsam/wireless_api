from flask import Flask
from flask import jsonify
from flask import request
from database import Database

app = Flask(__name__)

db = Database()

@app.route('/api/activities')
def activities():
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")
    activities = db.get_activities(start_time, end_time)
    return jsonify(activities)

if __name__ == '__main__':
    app.run()
