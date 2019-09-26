import time, sys, os
from datetime import datetime
import board
import busio
import adafruit_lsm9ds1
from daemon import Daemon

class MyDaemon(Daemon):
        def run(self):
            file_setup(cwd+"telemetry",headers) #Create new csv file with Header        
            while True:
                readSensors()    


def file_setup(filename, headers):
    filename = filename+"-"+str(datetime.now())+".csv"
    with open(filename,"w") as f:
        f.write(",".join(str(value) for value in headers)+ "\n")


def readSensors():
        # Read acceleration, magnetometer, gyroscope, temperature.
        accel_x, accel_y, accel_z = sensor.acceleration
        mag_x, mag_y, mag_z = sensor.magnetic
        gyro_x, gyro_y, gyro_z = sensor.gyro
        temp = sensor.temperature
        return accel_x, accel_y, accel_z, mag_x, mag_y, mag_z, gyro_x, gyro_y, gyro_z, temp
        # time.sleep(4.0)


headers = ["accel_x", "accel_y", "accel_z", "mag_x", "mag_y", "mag_z", "gyro_x", "gyro_y", "gyro_z", "temp"]

# I2C Sensor setup
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

cwd = os.getcwd()+"/" # Current Directory


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
