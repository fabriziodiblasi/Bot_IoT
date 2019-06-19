import serial
import telebot
import time
connected = False
port = 'COM3'
baud = 9600
ser = serial.Serial(port, baud, timeout=0)
out_file = open("dataset.txt", "a+")
for i in range(5000):
    while ser.inWaiting() > 0:
        data_str = ser.read(ser.inWaiting()).decode('ascii')
        # print("data_str ", data_str)
        # Scrive un file.
        val=''
        for x in data_str:
            if x != 'L' and x != 'H' and x != '_':
                # print("x : ",x)
                val = val + x
        print("Val : ", val)

        out_file.write(val+"\n")


    time.sleep(0.5)

out_file.close()