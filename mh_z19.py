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
      written_num = conn.write("\xff\x01\x86\x00\x00\x00\x00\x00\x79")
      conn.flush()
      time.sleep(0.5)

      response = conn.read(9)
      if len(response) == 9 and response[0] == "\xff" and response[1] == "\x86":
        return ord(response[2])*256 + ord(response[3])
    return None
  finally:
    conn.close()

if __name__ == '__main__':
  print str(mh_z19())
