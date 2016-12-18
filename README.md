# home-sensors
Reading team,humidity and co2  

Depends on  
https://github.com/adafruit/Adafruit_Python_DHT  


Getty has to be disabled:  
`sudo systemctl disable serial-getty@ttyAMA0.service`  

http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/  

sudo cp sensor-loop.service /lib/systemd/system/sensor-loop.service  

sudo chmod 644 /lib/systemd/system/sensor-loop.service  

sudo systemctl daemon-reload  
sudo systemctl enable sensor-loop.service  

sudo systemctl status sensor-loop.service  
