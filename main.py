import board
import digitalio
import busio
import adafruit_bus_device.i2c_device as i2c_device
from micropython import const
 

_LSM9DS1_ADDRESS_ACCELGYRO       = const(0x6B)
_LSM9DS1_ADDRESS_MAG             = const(0x1E)
_LSM9DS1_XG_ID                   = const(0b01101000)
_LSM9DS1_MAG_ID                  = const(0b00111101)
_LSM9DS1_ACCEL_MG_LSB_2G         = 0.061
_LSM9DS1_ACCEL_MG_LSB_4G         = 0.122
_LSM9DS1_ACCEL_MG_LSB_8G         = 0.244
_LSM9DS1_ACCEL_MG_LSB_16G        = 0.732
_LSM9DS1_MAG_MGAUSS_4GAUSS       = 0.14
_LSM9DS1_MAG_MGAUSS_8GAUSS       = 0.29
_LSM9DS1_MAG_MGAUSS_12GAUSS      = 0.43
_LSM9DS1_MAG_MGAUSS_16GAUSS      = 0.58
_LSM9DS1_GYRO_DPS_DIGIT_245DPS   = 0.00875
_LSM9DS1_GYRO_DPS_DIGIT_500DPS   = 0.01750
_LSM9DS1_GYRO_DPS_DIGIT_2000DPS  = 0.07000
_LSM9DS1_TEMP_LSB_DEGREE_CELSIUS = 8 # 1°C = 8, 25° = 200, etc.
_LSM9DS1_REGISTER_WHO_AM_I_XG    = const(0x0F)
_LSM9DS1_REGISTER_CTRL_REG1_G    = const(0x10)
_LSM9DS1_REGISTER_CTRL_REG2_G    = const(0x11)
_LSM9DS1_REGISTER_CTRL_REG3_G    = const(0x12)
_LSM9DS1_REGISTER_TEMP_OUT_L     = const(0x15)
_LSM9DS1_REGISTER_TEMP_OUT_H     = const(0x16)
_LSM9DS1_REGISTER_STATUS_REG     = const(0x17)
_LSM9DS1_REGISTER_OUT_X_L_G      = const(0x18)
_LSM9DS1_REGISTER_OUT_X_H_G      = const(0x19)
_LSM9DS1_REGISTER_OUT_Y_L_G      = const(0x1A)
_LSM9DS1_REGISTER_OUT_Y_H_G      = const(0x1B)
_LSM9DS1_REGISTER_OUT_Z_L_G      = const(0x1C)
_LSM9DS1_REGISTER_OUT_Z_H_G      = const(0x1D)
_LSM9DS1_REGISTER_CTRL_REG4      = const(0x1E)
_LSM9DS1_REGISTER_CTRL_REG5_XL   = const(0x1F)
_LSM9DS1_REGISTER_CTRL_REG6_XL   = const(0x20)
_LSM9DS1_REGISTER_CTRL_REG7_XL   = const(0x21)
_LSM9DS1_REGISTER_CTRL_REG8      = const(0x22)
_LSM9DS1_REGISTER_CTRL_REG9      = const(0x23)
_LSM9DS1_REGISTER_CTRL_REG10     = const(0x24)
_LSM9DS1_REGISTER_OUT_X_L_XL     = const(0x28)
_LSM9DS1_REGISTER_OUT_X_H_XL     = const(0x29)
_LSM9DS1_REGISTER_OUT_Y_L_XL     = const(0x2A)
_LSM9DS1_REGISTER_OUT_Y_H_XL     = const(0x2B)
_LSM9DS1_REGISTER_OUT_Z_L_XL     = const(0x2C)
_LSM9DS1_REGISTER_OUT_Z_H_XL     = const(0x2D)
_LSM9DS1_REGISTER_WHO_AM_I_M     = const(0x0F)
_LSM9DS1_REGISTER_CTRL_REG1_M    = const(0x20)
_LSM9DS1_REGISTER_CTRL_REG2_M    = const(0x21)
_LSM9DS1_REGISTER_CTRL_REG3_M    = const(0x22)
_LSM9DS1_REGISTER_CTRL_REG4_M    = const(0x23)
_LSM9DS1_REGISTER_CTRL_REG5_M    = const(0x24)
_LSM9DS1_REGISTER_STATUS_REG_M   = const(0x27)
_LSM9DS1_REGISTER_OUT_X_L_M      = const(0x28)
_LSM9DS1_REGISTER_OUT_X_H_M      = const(0x29)
_LSM9DS1_REGISTER_OUT_Y_L_M      = const(0x2A)
_LSM9DS1_REGISTER_OUT_Y_H_M      = const(0x2B)
_LSM9DS1_REGISTER_OUT_Z_L_M      = const(0x2C)
_LSM9DS1_REGISTER_OUT_Z_H_M      = const(0x2D)
_LSM9DS1_REGISTER_CFG_M          = const(0x30)
_LSM9DS1_REGISTER_INT_SRC_M      = const(0x31)
_MAGTYPE                         = True
_XGTYPE                          = False
_SENSORS_GRAVITY_STANDARD        = 9.80665

def read_register(register, length):
    with _i2c as i2c:
      i2c.write(bytes([register & 0xFF]))
      result = bytearray(length)
      i2c.readinto(result)
      print("$%02X => %s" % (register, [hex(i) for i in result]))
      return result

def write_register_byte(register, value):
    with _i2c as i2c:
      i2c.write(bytes([register & 0xFF, value & 0xFF]))
      print("$%02X <= 0x%02X" % (register, value))

 
# Try to create an I2C device
i2c_dev = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

_i2c = i2c_device.I2CDevice(i2c_dev, _LSM9DS1_ADDRESS_ACCELGYRO)


read_register(_LSM9DS1_REGISTER_WHO_AM_I_XG,1)


