import requests
import json
import datetime
import time
import queue
import threading
import certifi

from webserver import keep_alive

def createkey():
    from uuid import uuid4
    key = uuid4()
    return key

cert = certifi.where()

URL = "https://api.mojang.com/users/profiles/minecraft/"
URLG = "https://api.gapple.pw/cors/username/"

class Cycled(Exception): pass

def getq():
    with open("snipelist.json", "r", encoding="utf-8") as f:
        oglist = json.load(f)
        oglist = [x.lower() for x in oglist]
    q = queue.Queue()
    for i in oglist:
        q.put(i)
    return q


def retry(i, type="gapple"):
    if type == "mojang":
        url = URL
    elif type == "gapple":
        url = URLG
    else:
        raise ValueError("`type` must be either `mojang` or `gapple`")

    while True:
        r = requests.get(f"{url}{i}", headers={"Content-Type": "application/json"}, verify=cert)
        if r.status_code == 204:
            print(f"[{datetime.datetime.now()}] => {i}")
            break
        elif r.status_code == 429:
            print("429")
            time.sleep(5)
        elif r.status_code == 200:
            data = r.json()
            print(data)
            if "error" in data:
                time.sleep(5)
            else:
                break

def get(i, type="gapple"):
    if type == "mojang":
        url = URL
    elif type == "gapple":
        url = URLG
    else:
        raise ValueError("`type` must be either `mojang` or `gapple`")
    
    try:
        r = requests.get(f"{url}{i}", headers={"Content-Type": "application/json"}, verify=cert)
        if r.status_code == 204:
            print(f"[{datetime.datetime.now()}] => {i}")
            with open("data.json", "r") as f:
                json_object = json.load(f)
                keys = []
                for item in json_object:
                    key, value = list(item.items())[0]
                    keys.append(key)
                print(keys)
                if i not in keys:
                    data = json_object.append({i: {"datetime": str(datetime.datetime.now()), "unix": int(datetime.datetime.timestamp(datetime.datetime.now()))}})
                    with open("data.json", "w") as f:
                        json.dump(json_object, f, indent=3)
        elif r.status_code == 429:
            print("429")
            time.sleep(5)
            retry(type=type, i=i)
        elif r.status_code == 200:
            data = r.json()
            print(data)
            if "error" in data:
                time.sleep(2)
                retry(type=type, i=i)
    except Exception as e:
        print(f"EXCEPTION: {e}")


def main(queue: queue.Queue, type: str = "gapple"):
    while not queue.empty():
        i = queue.get()
        get(i=i, type=type)


if __name__ == '__main__':
    keep_alive()
    while True:
        q = getq()
        threads = []
        for _ in range(3):
            thread = threading.Thread(target=main, args=(q, "gapple"))
            time.sleep(3)
            thread.start()
            threads.append(thread)
        for _ in range(2):
            thread = threading.Thread(target=main, args=(q, "mojang"))
            time.sleep(3)
            thread.start()
            threads.append(thread)
        for i in threads:
            i.join()
        print("CYCLED")

