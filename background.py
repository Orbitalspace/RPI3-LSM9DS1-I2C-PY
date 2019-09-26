import time, sys
import board
import busio
import adafruit_lsm9ds1
from daemon import Daemon

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_lsm9ds1.LSM9DS1_I2C(i2c)

class MyDaemon(Daemon):
        def run(self):
                while True:
                    readSensors()    
                

def file_setup(filename):
  header =["accel_x", "accel_y", "accel_z", "mag_x", "mag_y", "mag_z", "gyro_x", "gyro_y", "gyro_z", "temp"]
  with open(filename,"w") as f:
    f.write(",".join(str(value) for value in header)+ "\n")


def readSensors():
        # Read acceleration, magnetometer, gyroscope, temperature.
        accel_x, accel_y, accel_z = sensor.acceleration
        mag_x, mag_y, mag_z = sensor.magnetic
        gyro_x, gyro_y, gyro_z = sensor.gyro
        temp = sensor.temperature
        # Print values.
        print('Acceleration (m/s^2): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(accel_x, accel_y, accel_z))
        print('Magnetometer (gauss): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(mag_x, mag_y, mag_z))
        print('Gyroscope (degrees/sec): ({0:0.3f},{1:0.3f},{2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
        print('Temperature: {0:0.3f}C'.format(temp))
        # Delay for a second.
        time.sleep(1.0)

       

if __name__ == "__main__":
        daemon = MyDaemon('/tmp/daemon-example.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        file_setup("telemetry.csv") #Create new csv file with Header        
                        readSensors() # Sanity Check print sensor values
                        daemon.start()# Start the background service

                elif 'stop' == sys.argv[1]:
                        daemon.stop()
                elif 'restart' == sys.argv[1]:
                        daemon.restart()
                else:
                        print("Unknown command")
                        sys.exit(2)
                sys.exit(0)
        else:
                print ("usage: %s start|stop|restart" % sys.argv[0])
                sys.exit(2)
