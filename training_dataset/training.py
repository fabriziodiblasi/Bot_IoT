import serial
import telebot
import time
import os; os.environ["OMP_NUM_THREADS"] = "4"

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

import keras
import keras.backend as K




stato = 0
# uso questa variabile per scegliere cosa fare
# 0 - traino la rete neurale
# 1 - uso la RNN per prevedere il prossimo valore
# 2 - aggiungo valori al dataset


if stato == 0:
    train_df = pd.read_csv("dataset.csv", sep=",")
    print(train_df.shape)
    print(train_df)
    train, dev = train_test_split(train_df, random_state=123, shuffle=True, test_size=0.1)
    print("Training data shape:", train.shape)
    print("Test data shape:", dev.shape)



if stato == 2:

    connected = False
    port = 'COM3'
    baud = 9600
    ser = serial.Serial(port, baud, timeout=0)
    time.sleep(2)

    for i in range(5000):
        while ser.inWaiting() > 0:
            out_file = open("dataset.csv", "a+")
            data_str = ser.read(ser.inWaiting()).decode('ascii')
            # print("data_str ", data_str)
            # Scrive un file.
            val = ''
            for x in data_str:
                if x != 'a' and x != 'w' and x != '_':
                    # print("x : ",x)
                    val = val + x
            if val != '':
                print("Valore letto : ", val)
                out_file.write('"' + val + '"' + "\n")
                out_file.close()
        time.sleep(0.5)
