from dht22 import dht22
from mh_z19 import mh_z19

import time
import sqlite3

conn = sqlite3.connect('/home/pi/sensor-data.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS log (temperature DOUBLE, humidity DOUBLE, CO2 INTEGER, timestamp INTEGER)")


try:
  while True:
    try:
      co2 = mh_z19()
      humidity, temperature = dht22()
    
      print('Temp={0:0.1f}*  Humidity={1:0.1f}% CO2={2:d}'.format(temperature, humidity, co2))

      c.execute("INSERT INTO log VALUES (?,?,?,?)", (temperature, humidity, co2, int(time.time())))
      conn.commit()
    except:
      print('Reading failed, will retry in a minute')
    finally:
      time.sleep(60)
finally:
  conn.close()
