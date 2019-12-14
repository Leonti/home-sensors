import os
import sys
import traceback
import led_stripe
import ac

RESIN = os.environ.get("RESIN", None)

if RESIN == "1":
  from dht22 import dht22
  from mh_z19 import mh_z19
  from dust import read_sds011

import time
from pymongo import MongoClient

mongoClient = MongoClient(os.environ.get("MONGO_HOST_PORT", None))
mongoClient[os.environ.get("MONGO_DB", None)].authenticate(os.environ.get("MONGO_USERNAME", None), os.environ.get("MONGO_PASSWORD", None), mechanism='SCRAM-SHA-1')
db = mongoClient[os.environ.get("MONGO_DB", None)]
readings = db['readings']
dust_readings = db['readings']
commands = db['commands']
latest = db['latest']
latest_dust = db['latest_dust']
#arduinoConn = led_stripe.connectToArduino()

def collect_and_send_readings():
  co2 = mh_z19()
  humidity, temperature = dht22()

  print('Temp={0:0.1f}*  Humidity={1:0.1f}% CO2={2:d}'.format(temperature, humidity, co2))
  entry = {"temperature": temperature,
           "humidity": humidity,
           "co2": co2,
           "timestamp": int(time.time())}
  readings.insert_one(entry)
  entry['_id'] = 'latest'
  latest.find_one_and_replace({'_id': 'latest'}, entry, upsert = True)

def collect_and_send_dust_readings():
  (pm2_5, pm10) = read_sds011()

  print('pm2.5={0:0.1f}*  pm10={1:0.1f}%'.format(pm2_5, pm10))
  entry = {"pm2_5": pm2_5,
           "pm10": pm10,
           "timestamp": int(time.time())}
  dust_readings.insert_one(entry)
  entry['_id'] = 'latest'
  latest_dust.find_one_and_replace({'_id': 'latest'}, entry, upsert = True)

def handle_command(command):
 # global arduinoConn
  if command['type'] == 'LED':
#    if arduinoConn == None:
#      arduinoConn = led_stripe.connectToArduino()
    print('LED command')
    data = command['data']
#    led_stripe.send_rgb(arduinoConn, data['r'], data['g'], data['b'])
  elif command['type'] == 'AC':
    print('AC command')
    ac.send_command(command['data'])

counter = 0
try:
    while True:
      try:
        for command in commands.find({}):
          print("Handling a command")
          print(command['type'])
          commands.delete_one({'_id': command['_id']})
          handle_command(command)

        if counter % 60 == 0:
          if RESIN == "1":
            collect_and_send_readings()
          else:
            print("collecting readings")
        if counter % 300 == 0:
          if RESIN == "1":
            collect_and_send_dust_readings()
          else:
            print("collecting dust readings")            
      except:
        print("Reading failed, will retry in a minute:", sys.exc_info()[0])
        traceback.print_exc()
      finally:
        time.sleep(1)
        counter += 1
        if counter == 300:
          counter = 0
finally:
#  arduinoConn.close()
  print("Finished")
