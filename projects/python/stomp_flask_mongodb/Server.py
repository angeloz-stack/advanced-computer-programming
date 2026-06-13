from flask import Flask, request
import pymongo
import logging

app = Flask(__name__)

client = pymongo.MongoClient("localhost", 27017)
db = client["database"]
bookings = db["bookings"]

@app.post("/bookings")
def book():

    data = request.get_json()
    try:
        bookings.insert_one(data)
    except Exception as e:
        response = "DATABASE ERROR"
        status = 500
    else:
        logging.info(f"Salvata {data}")
        response = "OK"
        status = 200

    return response, status

@app.put("/bookings/update")
def apply_discount():

    data = request.get_json()
    try:
        for booking in bookings.find({
                "operator": data["operator"], 
                "nights": {"$gte": data["nights"]}}):
            new_cost = max(booking["cost"] - data["discount"], 0)
            logging.info(f"Aggiorno : {booking} - Costo prima: {booking["cost"]}, Costo dopo: {new_cost}")
            bookings.update_one({"_id": booking["_id"]}, {"$set": {"cost": new_cost}})
    except Exception as e:
        response = "DATABASE ERROR"
        status = 500
    else:
        response = "OK"
        status = 200
    
    return response, status

def main():
    logging.basicConfig(
        format="[SERVER] - %(message)s",
        level=logging.INFO
    )
    app.run(port=2222, debug=True)

if __name__ == "__main__":
    main()