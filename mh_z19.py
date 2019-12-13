# http://eleparts.co.kr/data/design/product_file/SENSOR/gas/MH-Z19_CO2%20Manual%20V2.pdf
# http://qiita.com/UedaTakeyuki/items/c5226960a7328155635f
import serial
import time

def mh_z19():
  conn = serial.Serial('/dev/ttyAMA0',
                      baudrate=9600,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=1.0)

  try:
    for x in range(0, 10):
      written_num = conn.write(b"\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      conn.flush()
      time.sleep(0.5)

      response = conn.read(9)
      if len(response) == 9 and response[0] == int.from_bytes(b'\xff', byteorder='big') and response[1] == int.from_bytes(b'\x86', byteorder='big'):
        return response[2]*256 + response[3]
    return None
  finally:
    conn.close()

if __name__ == '__main__':
  print(str(mh_z19()))
