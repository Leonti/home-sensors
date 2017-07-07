import os

RESIN = os.environ.get("RESIN", None)

if RESIN == "1":
  from dht22 import dht22
  from mh_z19 import mh_z19

import time
from pymongo import MongoClient

mongoClient = MongoClient(os.environ.get("MONGO_HOST_PORT", None))
mongoClient[os.environ.get("MONGO_DB", None)].authenticate(os.environ.get("MONGO_USERNAME", None), os.environ.get("MONGO_PASSWORD", None), mechanism='SCRAM-SHA-1')
db = mongoClient[os.environ.get("MONGO_DB", None)]
collection = db['readings']

try:
  while True:
    try:
      co2 = mh_z19()
      humidity, temperature = dht22()

      print('Temp={0:0.1f}*  Humidity={1:0.1f}% CO2={2:d}'.format(temperature, humidity, co2))
      entry = {"temperature": temperature,
               "humidity": humidity,
               "co2": co2,
               "timestamp": int(time.time())}
      collection.insert_one(entry)
    except:
      print('Reading failed, will retry in a minute')
    finally:
      time.sleep(60)
finally:
    print("Finished")
