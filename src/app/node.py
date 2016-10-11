#python2.7
import os
from socket import *
from pymongo import *
import json
from pymongo import MongoClient
import time

def read_config():
    with open('pi.cfg') as json_data:
        cfg = json.load(json_data)

    global port
    global bay
    global store
    global uri
    port = int(cfg["port"])
    bay = cfg["bay"]
    store = cfg["store"]
    uri = cfg["mongo"]
    print("config read.")

def config_mongo():
    client = MongoClient(uri)
    global db
    db = client.store
    print("mongo configured.")


def config_socket():
    global buf
    global UDPSock
    host = ""
    buf = 1024
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    UDPSock.bind(addr)
    print("socket configured.")

def init():
    read_config()
    config_mongo()
    config_socket()
    print("configuration successful.")

def add_element(collectionName, bayId, trolleyId):
    print("update trolley " + trolleyId+" in "+bayId)
    collection = db[collectionName]
    cursor = db[collectionName].find({"bayid": bayId, "trolleyid": trolleyId, "outtime": "x"})
    toIn = (cursor.count() == 0)
    cursor.close()
    if toIn:
        result = collection.insert_one({
            "bayid": bayId,
            "trolleyid": trolleyId,
            "intime": int(time.time()),
            "outtime": "x"
        })
        result.inserted_id
    if toIn == False:
        result = collection.update_one(
            {"bayid": bayId,  "trolleyid": trolleyId, "outtime": "x"},
            {"$set": {"outtime": int(time.time())}}
        )
    print("Added element.")


init()
print("\nServer started...")
while True:
    (data, addr) = UDPSock.recvfrom(buf)
    print "Received(" + data +")"
    if "trollid:" in data:
        data = data.split("trollid:")[1]
        try:

            add_element(store,bay,data)
        except :
            print "invalid message recieved"

UDPSock.close()
os._exit(0)
