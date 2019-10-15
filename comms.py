#!/usr/bin/python3
# Taken from: https://thomask.sdf.org/blog/2018/12/15/sending-raw-ax25-python.html and https://thomask.sdf.org/code/send_kiss_frame.py, made minor changes to make it work.
import sys
import socket
import serial
import time

#Connection Modes
_TCP_CONN = 0x01
_UART_CONN = 0x02

# Addresses must be 6 bytes plus the SSID byte, each character shifted left by 1
# If it's the final address in the header, set the low bit to 1
# Ignoring command/response for simple example
def encode_address(s, final):
    if "-" not in s:
        s = s + "-0"    # default to SSID 0
    call, ssid = s.split('-')
    if len(call) < 6:
        call = call + " "*(6 - len(call)) # pad with spaces
    encoded_call = [ord(x) << 1 for x in call[0:6]]
    encoded_ssid = (int(ssid) << 1) | 0b01100000 | (0b00000001 if final else 0)
    return encoded_call + [encoded_ssid]


def send(method,src_addr, dest_addr,msg ):

    KISS_FEND = 0xC0    # Frame start/end marker
    KISS_FESC = 0xDB    # Escape character
    KISS_TFEND = 0xDC   # If after an escape, means there was an 0xC0 in the source message
    KISS_TFESC = 0xDD   # If after an escape, means there was an 0xDB in the source message

    # Make a UI frame by concatenating the parts together
    # This is just an array of ints representing bytes at this point
    dest_addr = encode_address(dest_addr.upper(), False)
    src_addr = encode_address(src_addr.upper(), True)
    c_byte = [0x03]           # This is a UI frame
    pid = [0xF0]              # No protocol
    msg = [ord(c) for c in msg]
    packet = dest_addr + src_addr + c_byte + pid + msg

    # Escape the packet in case either KISS_FEND or KISS_FESC ended up in our stream
    packet_escaped = []
    for x in packet:
        if x == KISS_FEND:
            packet_escaped += [KISS_FESC, KISS_TFEND]
        elif x == KISS_FESC:
            packet_escaped += [KISS_FESC, KISS_TFESC]
        else:
            packet_escaped += [x]

    # Build the frame that we will send to Dire Wolf and turn it into a string
    kiss_cmd = 0x00 # Two nybbles combined - TNC 0, command 0 (send data)
    kiss_frame = [KISS_FEND, kiss_cmd] + packet_escaped + [KISS_FEND]
    output = bytearray(kiss_frame)
    
    if method ==  _TCP_CONN:
        # Connect to Dire Wolf listening on port 8001 on this machine and send the frame
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.43.68", 8002))
        s.send(output)
        s.close()
    elif method == _UART_CONN:
        ser = serial.Serial(            
            port='/dev/ttyAMA0',
            baudrate = 115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        while 1:
            print(kiss_frame)
            #ser.write(str.encode(kiss_frame+'\r\n'))
            ser.write(kiss_frame)
            time.sleep(1)

    else:
        print("Unkown Method")


#send(_UART_CONN,"CALLSIGN","OBC","Telemetry")


