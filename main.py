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
with open("oglist.json", "r", encoding="utf-8") as f:
    oglist = json.load(f)
    oglist = [x.lower() for x in oglist]
q = queue.Queue()
for i in oglist:
    q.put(i)

with open("valid_proxies.json", "r", encoding="utf-8") as f:
    proxies = json.load(f)


async def send(letter:str = "All"):
    if letter != "All":
        with open(f"oglist_{letter}.json", "r", encoding="utf-8") as f:
            oglist = json.load(f)
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('WEBHOOK', session=session)
        global q
        count = 1
        proxy = proxies[count]
        await webhook.send(f"**{letter}** -> Started cycle, using proxy: `{proxy}`")
        for i in oglist:
                try:            
                    r = requests.get(f"{URL}{i}", headers={"Content-Type": "application/json"}, proxies={"http": proxy, "https": proxy}, verify=cert)
                    if r.status_code == 204:
                        await webhook.send(f"> :star2: [{datetime.datetime.now()}] => `{i}`")
                    elif r.status_code == 429:
                        count = count + 1
                        proxy = proxies[count]
                        await webhook.send(f"> :exclamation: GOT 429, CHANGED PROXY TO `{proxy}`")
                        await webhook.send(f"> SKIPPING `{i}`")
                    elif r.status_code == 200:
                        data = r.json()
                        print(data)
                        if "error" in data:
                            await webhook.send(data)
                            count = count + 1
                            proxy = proxies[count]
                            await webhook.send(f"> :exclamation: GOT AN ERROR, CHANGED PROXY TO `{proxy}`")
                            await webhook.send(f"> SKIPPING `{i}`")
                except Exception as e:
                    await webhook.send(f"EXCEPTION: ||`{e}`||")
                    count = count + 1
                    proxy = proxies[count]
                    await webhook.send(f"> :exclamation: GOT AN EXCEPTION, CHANGED PROXY TO `{proxy}`")
                    await webhook.send(f"> SKIPPING `{i}`")

async def main():
    while True:
        await send("a")      

if __name__ == '__main__':
    asyncio.run(main())