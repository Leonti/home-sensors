from dht22 import dht22
from mh_z19 import mh_z19

co2 = mh_z19()
humidity, temperature = dht22()

print('Temp={0:0.1f}*  Humidity={1:0.1f}% CO2={2:d}'.format(temperature, humidity, co2))

