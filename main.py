#!/usr/bin/python3

import time, sys, os
from datetime import datetime
import board
import busio
import adafruit_lsm9ds1
from daemon import Daemon
from comms import send, encode_address
_TCP_CONN = 0x01
_UART_CONN = 0x02

LOG_FREQUENCY = 3

class MyDaemon(Daemon):
    def run(self):
        file_setup(cwd+"telemetry",headers) #Create new csv file with Header        
        while True:
            if 1==1:
                log_data(readSensors())


def log_data(sensor_data):
    global filename, batch_data
    batch_data.append(",".join([str(value) for value in sensor_data]))
    if len(batch_data) >= LOG_FREQUENCY:
        print(batch_data)
        #s = ["".join(x) for x in batch_data]
        #print(s)
        
        send(_TCP_CONN,"9K2S", "OBC", batch_data[0]) #[s.join(x) for x in batch_data])

        with open(filename, "a") as f:
            for line in batch_data:
                f.write(line + "\n")
        batch_data = []


def file_setup(fileName, headers):
    global filename
    filename = fileName+"-"+str(datetime.now())+".csv"
    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in headers)+ "\n")


def readSensors():
    accel_x, accel_y, accel_z = sensor.acceleration
    mag_x, mag_y, mag_z = sensor.magnetic
    gyro_x, gyro_y, gyro_z = sensor.gyro
    temp = sensor.temperature
    time.sleep(1.0)
    return float("%.3f" % float(accel_x)), float("%.3f" % float(accel_y)), float("%.3f" % float(accel_z)), float("%.3f" % float(mag_x)), float("%.3f" % float(mag_y)), float("%.3f" % float(mag_z)), float("%.3f" % float(gyro_x)), float("%.3f" % float(gyro_y)), float("%.3f" % float(gyro_z)), float("%.3f" % float(temp))

# Global Vars
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

cwd = os.getcwd()+"/" # Current Directory
batch_data = []
filename = ""
headers = ["accel_x", "accel_y", "accel_z", "mag_x", "mag_y", "mag_z", "gyro_x", "gyro_y", "gyro_z", "temp"]

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/obc-daemon.pid') # Unique id to prevent multiple copies running
    if len(sys.argv) == 2:
            if 'start' == sys.argv[1]:
                print("Starting")
                
                # Confirm Sensors Working
                accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, temp = readSensors()
                print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
                print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
                print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
                print('Temperature: {0:0.3f}C'.format(temp))
                
                # Start the Background Service
                daemon.start()  

            elif 'stop' == sys.argv[1]:
                    print("Stopping")
                    daemon.stop()
            elif 'restart' == sys.argv[1]:
                    print("Restarting")
                    daemon.restart()
            else:
                    print("Unknown command")
                    sys.exit(2)
            sys.exit(0)
    else:
            print ("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
