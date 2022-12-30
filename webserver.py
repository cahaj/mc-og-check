from flask import Flask
from flask import request
from threading import Thread
import json
import requests

app = Flask('')

with open("secrets.json", "r") as f:
    s = json.load(f)
URL = s["url"]

@app.route('/')
def home():
    return "Online."

@app.route('/data', methods=['GET'])
def data():
    key = request.args.get('key')
    r = requests.get(f"{URL}?key={key}")
    data = r.json()
    if "error" not in data:
        with open("data.json", "r") as f:
            data = json.load(f)
        return data
    else:
        return {"error": "InvalidKey"}

def run():
  app.run(host='0.0.0.0',port=6363)

def keep_alive():  
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    run()