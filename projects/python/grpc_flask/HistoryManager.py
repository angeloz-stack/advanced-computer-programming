from flask import Flask, request
import logging
import os

app = Flask(__name__)
FILENAME = "history.txt"

@app.post("/update_history")
def update_history():

    data = request.get_json()

    if "sell" not in data["operation"] or "buy" not in data["operation"]:
        response = "OPERATION NOT ALLOWED"
        status = 400
    elif data["operation"] == "sell" and not isinstance(data["serial_number"], int):
        response = "INVALID ID FOR SELL"
        status = 400
    else:
        response = "OK"
        status = 200

    #logging.info(data)

    with open(FILENAME, "a") as f:
        f.write(str(data) + "\n")
    
    return "OK", 200


def main():
    logging.basicConfig(
        filename="history.log",
        format="%(asctime)s - %(message)s",
        level=logging.INFO)
    
    app.run(debug=True)

if __name__ == "__main__":
    main()