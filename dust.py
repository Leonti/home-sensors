import time
import sds011

sensor = sds011.SDS011("/dev/ttyUSB0", use_query_mode=False)

def read_sds011():
  sensor.sleep(sleep=False)
  time.sleep(15)
  result = sensor.query()
  sensor.sleep(sleep=True)
  return result

if __name__ == '__main__':
  (pm2_5, pm10) = read_sds011()
  print(pm2_5)
  print(pm10)
