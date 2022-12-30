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

with open("oglist/oglist.json", "r", encoding="utf-8") as f:
    oglist = json.load(f)
    oglist = [x.lower() for x in oglist]
q = queue.Queue()
for i in oglist:
    q.put(i)

def getq(letter:str):
    with open(f"oglist/oglist_{letter}.json", "r", encoding="utf-8") as f:
        oglist = json.load(f)
    q = queue.Queue()
    for i in oglist:
        q.put(i)
    return q

with open("valid_proxies.json", "r", encoding="utf-8") as f:
    proxies = json.load(f)

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


def main(queue=None, type="mojang"):
    if queue != None:
        while not queue.empty():
            i = queue.get()
            get(i=i, type=type)  

    else:
        global q
        while not q.empty():
            i = q.get()
            get(i=i, type=type)   
    


if __name__ == '__main__':
    for _ in range(10):
        threading.Thread(target=main, args=(None, "gapple")).start()
        time.sleep(4)