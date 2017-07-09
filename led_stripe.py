import serial
import time

def connectToArduino():
  conn = serial.Serial('/dev/ttyUSB0', 115200)
  wait_for_connection(conn)

  return conn

def send_rgb(conn, r, g, b):
  command = ','.join([str(r), str(g), str(b)] * 4) + 'e'
  conn.write(bytes(command, encoding='UTF-8'))
  conn.flush()

def wait_for_connection(conn):
  buf = b''
  for x in range(0, 20):
    time.sleep(0.5)
    if conn.inWaiting() > 0:
      while conn.inWaiting() > 0:
        buf += conn.read(conn.inWaiting())
        print(str(buf))
      if buf == b'READY\r\n':
        return None

if __name__ == '__main__':
  conn = connectToArduino()
  try:
    print(send_rgb(conn, 0, 0, 0))
#    print(send_rgb(conn, 93, 237, 45))
  finally:
    conn.close()
