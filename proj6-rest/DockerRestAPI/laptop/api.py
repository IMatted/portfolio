# Laptop Service

import os
from datetime import datetime
from flask import Flask, request, Response, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient

# Instantiate the app
app = Flask(__name__)
api = Api(app)

client = MongoClient(os.environ.get('DB_PORT_27017_TCP_ADDR', 'db'), 27017)
db = client.brevetsdb
collection = db.brevets_list

def get_stored_data():
    data = collection.find_one({}, sort=[('_id', -1)])
    return data if data else {"times": []}

def process_controls(control_type, top_k=None):
    all_submissions = collection.find()
    
    if top_k is not None:
        flat_controls = []
        for submission in all_submissions:
            for c in submission.get("times", []):
                if not c.get("open") and not c.get("close"):
                    continue
                if control_type == "open":
                    flat_controls.append({"open": c.get("open")})
                elif control_type == "close":
                    flat_controls.append({"close": c.get("close")})
                else:
                    flat_controls.append({"open": c.get("open"), "close": c.get("close")})
                    
        sort_key = "close" if control_type == "close" else "open"
        try:
            flat_controls = sorted(
                flat_controls, 
                key=lambda x: datetime.strptime(x[sort_key], "%a %m/%d %H:%M")
            )
        except (KeyError, ValueError, TypeError):
            pass
            
        try:
            k = int(top_k)
            return flat_controls[:k]
        except (ValueError, TypeError):
            return flat_controls

    results = []
    for submission in all_submissions:
        controls = submission.get("times", [])
        submission_controls = []
        
        for c in controls:
            if not c.get("open") and not c.get("close"):
                continue
            if control_type == "open":
                submission_controls.append({"open": c.get("open")})
            elif control_type == "close":
                submission_controls.append({"close": c.get("close")})
            else:
                submission_controls.append({"open": c.get("open"), "close": c.get("close")})
        
        if submission_controls:
            results.append({
                "controls": submission_controls
            })
            
    return results

# Restful API Resources

class ListAll(Resource):
    def get(self, format_type=None):
        top_k = request.args.get("top")
        data = process_controls("all", top_k)
    
        if format_type == "csv":
            csv_lines = ["brevets/controls/open,brevets/controls/close"]
            if top_k is not None:
                for row in data:
                    csv_lines.append(f"{row['open']},{row['close']}")
            else:
                for submission in data:
                    for row in submission["controls"]:
                        csv_lines.append(f"{row['open']},{row['close']}")
            return Response("\n".join(csv_lines), mimetype="text/csv")

        return {"brevets": data}

class ListOpenOnly(Resource):
    def get(self, format_type=None):
        top_k = request.args.get("top")
        data = process_controls("open", top_k)

        if format_type == "csv":
            csv_lines = ["brevets/controls/open"]
            if top_k is not None:
                for row in data:
                    csv_lines.append(f"{row['open']}")
            else:
                for submission in data:
                    for row in submission["controls"]:
                        csv_lines.append(f"{row['open']}")
            return Response("\n".join(csv_lines), mimetype="text/csv")
            
        return {"brevets": data}

class ListCloseOnly(Resource):
    def get(self, format_type=None):
        top_k = request.args.get("top")
        data = process_controls("close", top_k)
        
        if format_type == "csv":
            csv_lines = ["brevets/controls/close"]
            if top_k is not None:
                for row in data:
                    csv_lines.append(f"{row['close']}")
            else:
                for submission in data:
                    for row in submission["controls"]:
                        csv_lines.append(f"{row['close']}")
            return Response("\n".join(csv_lines), mimetype="text/csv")
        
        return {"brevets": data}
    
api.add_resource(ListAll, '/listAll', '/listAll/<string:format_type>')
api.add_resource(ListOpenOnly, '/listOpenOnly', '/listOpenOnly/<string:format_type>')
api.add_resource(ListCloseOnly, '/listCloseOnly', '/listCloseOnly/<string:format_type>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)