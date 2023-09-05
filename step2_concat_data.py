# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 20:56:45 2023

@author: sfelc
"""

import pandas as pd
import numpy as np

data0 = pd.read_csv("Stacje/data0.csv")
HMD = pd.DataFrame(data = [np.array(data0["Dostępne rowery"])], columns = data0["Numer stacji"])
time_temp = pd.DataFrame({'time': [data0["time"][0]]})
HMD = pd.concat([time_temp, HMD], axis = 1)

f = open("metadata.txt","r")
n = int(f.readline())
n2 = int(f.readline())
f.close()

for i in range(1,n):
    namestring = "Stacje/data" + str(i) + ".csv"
    data_temp = pd.read_csv(namestring)
    if len(data_temp)  == 243:
        print (i)
        data_temp = data_temp.drop(242)
    HMD_temp = pd.DataFrame(data = [np.array(data_temp["Dostępne rowery"])], columns = data_temp["Numer stacji"])
    time_temp = pd.DataFrame({'time': [data_temp["time"][0]]})
    HMD_temp = pd.concat([time_temp, HMD_temp], axis = 1)
    HMD = pd.concat([HMD, HMD_temp], ignore_index = True)
    
HMD.to_csv("HeatMap_data.csv")