import requests
import json
import discord
from discord import Webhook
import aiohttp
import asyncio
import datetime
import time
import queue
import threading
import random
import certifi

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


def retry(type, i):
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

def get(i, type="mojang"):
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


q = getq()
def main(queue: queue.Queue, type: str = "gapple"):
    while not queue.empty():
        i = queue.get()
        get(i=i, type=type)


if __name__ == '__main__':
    while True:
        q = getq()
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=main, args=(q, "gapple"))
            thread.start()
            threads.append(thread)
        for i in threads:
            i.join()
        print("CYCLED")

