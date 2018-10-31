#!/usr/bin/env python

import os
import requests
from requests.exceptions import ConnectionError
import json
import time

def main():
    server = os.environ.get("SERVER")
    kairos = os.environ.get("KAIROS")
    agreement = os.environ.get("AGREEMENT")
    print("server={}, kairos={}, agreement={}".format(server, kairos, agreement))

    try:
        r = requests.get(server)
        delta = r.elapsed.total_seconds() * 1000

        print("{} GET {} {} ms".format(r.status_code, server, delta))

        send_metrics(kairos, agreement, responseTime=delta, alive=1 if r.status_code < 500 else 0)

    except ConnectionError as e:
        print(e.message)
        send_metrics(kairos, agreement, alive=0)

def send_metrics(kairos, agreement, timestamp=None, responseTime=None, alive=None):
    if responseTime is None and alive is None:
        raise ValueError("alive and responseTime cannot be both None")
    if timestamp is None:
        timestamp = int(time.time() * 1000)

    data = []
    tags = { "agreement" : agreement }

    if responseTime is not None:
        data.append(metric("responseTime", responseTime, timestamp, tags))
    if alive is not None:
        data.append(metric("alive", alive, timestamp, tags))
    
    url = "{}/api/v1/datapoints".format(kairos)
    r = requests.post(url, json=data)
    if r.status_code >= 400:
        print(r.json())
    else:
        print("{} POST {}".format(r.status_code, r.url))
        print(json.dumps(data))

def metric(key, value, timestamp, tags):
    return { "name": key, "value": value, "timestamp": timestamp, "tags": tags }

if __name__ == "__main__":
    main()
