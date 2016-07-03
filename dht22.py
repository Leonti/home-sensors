import sys
import Adafruit_DHT

def dht22():
  return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 22)

if __name__ == '__main__':
  humidity, temperature = dht22()
  print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))

