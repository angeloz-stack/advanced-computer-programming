from flask import Flask, request
import pymongo
from pymongo.errors import DuplicateKeyError

DATA_TYPES = ["temp", "press"]
DATATYPE_COLLECTION_MAPPING = {
     "temp": "temp_data",
     "press": "press_data"
}

app = Flask(__name__)

client = pymongo.MongoClient("localhost", 27017)
db = client["database"]


@app.post("/sensor")
def add_sensor():
    data = request.get_json()

    collection = db["sensors"]

    response = {}
    status = None

    try:
        collection.insert_one(data)
        response["result"]= "success"
        status = 201
    except DuplicateKeyError:
        response["result"]= "Sensor already in database"
        status = 409

    return response, status

@app.post("/data/<data_type>")
def add_measure(data_type):

    response = {}
    status = None

    if data_type not in DATA_TYPES:
        return {"result": "invalid data type"}, 400
    
    data = request.get_json()
    
    collection = db[DATATYPE_COLLECTION_MAPPING[data_type]]

    try:
        collection.insert_one(data)
        response["result"]= "success"
        status = 201
    except DuplicateKeyError:
        response["result"]= "Data already in database"
        status = 409

    return response, status

if __name__ == "__main__":
    app.run(debug=True)