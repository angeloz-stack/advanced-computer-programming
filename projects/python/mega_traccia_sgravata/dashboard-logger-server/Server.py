from flask import Flask, request
import pymongo
from statistics import mean

app = Flask(__name__)

client = pymongo.MongoClient("localhost", 27017)
db = client["database"]
collection = db["alerts"]

@app.post("/alert")
def add_alert():
    data = request.get_json()

    try:
        collection.insert_one(data)
    except Exception:
        status = 500
        response = "DATABASE ERROR"
    else:
        status = 201
        response = "OK"
    
    return response, status

@app.get("/stats/<zone>")
def stats_per_zone(zone):

    results = list(collection.find({"zone": zone}))

    if not results:
        return {"zone": zone, "n_of_alerts": 0, "avg_reading": 0}, 404

    n_of_alerts = len(results)
    avg = mean([result["reading"] for result in results])

    return {"zone": zone, "n_of_alerts": n_of_alerts, "avg_reading": avg}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5001)