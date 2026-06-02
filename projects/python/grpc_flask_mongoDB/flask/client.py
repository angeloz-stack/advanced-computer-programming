import requests
import threading
import random
from controller import DATA_TYPES
import logging

SERVER_ADDRESS = "http://127.0.0.1:5000" # server flask

def thd_func(id: int, data_type: str):
    data = {"_id": id, "data_type": data_type}
    response = requests.post(SERVER_ADDRESS+"/sensor", json=data)
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        logging.warning(f"[SENSOR-{id}] Errore: Ricevuto {response.status_code} - {response.text}")
    else:
        logging.info(f"Registrato sensor_id= {id} data_type={data_type}")

    for i in range(5):
        value = random.randint(1, 50)
        data = {"sensor_id": id, "data": value}
        response = requests.post(SERVER_ADDRESS+f"/data/{data_type}", json=data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.warning(f"[SENSOR-{id}] Errore: Ricevuto {response.status_code} - {response.text}")
        else:
            logging.info(f"Inviata misurazione sensor_id= {id} data={value}")

def main():

    logging.basicConfig(
        format="[CLIENT] [%(threadName)s] - %(levelname)s - %(message)s",
        level=logging.INFO)
    
    threads = []

    for i in range(1,6):
        
        t = threading.Thread(target=thd_func, args=(i, random.choice(DATA_TYPES)))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()