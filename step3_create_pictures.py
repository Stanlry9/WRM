# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 00:14:45 2023

@author: sfelc
"""

# takes a long time, possible memory leak

import matplotlib.pyplot as plt
import shapefile
import pandas as pd
import numpy as np

data = pd.read_csv("HeatMap_data.csv").drop(["Unnamed: 0"], axis = 1)
locs = pd.read_csv("locs.csv")
locs = locs.drop(["Unnamed: 0", "Dostępne rowery", "Numery dostępnych rowerów"], axis = 1)
data_locs = data.rename(columns={str(15001): locs.loc[locs["Numer stacji"] == 15001].iat[0, 2]})

for i in range(15001, 15310):
    if str(i) in data_locs.columns.values:
        data_locs = data_locs.rename(columns={str(i): locs.loc[locs["Numer stacji"] == i].iat[0, 2]})

# locslist = list(locs["Współrzędne"])

plt.rcParams['figure.dpi'] = 300

def normal_pdf(x, mean, var):
    return np.exp(-(x - mean)**2 / (2*var))

N = 1000
xmin, xmax, ymin, ymax = (16.80, 17.18, 51.02, 51.22)
nmax = 51.2114720
smax = 51.0426932
wmax = 16.8071251
emax = 17.1763221

xx = np.linspace(xmin, xmax, N)
yy = np.linspace(ymin, ymax, N)

shpFilePath = "GraniceOsiedli/GraniceOsiedli.shp"  
listx=[]
listy=[]
sf = shapefile.Reader(shpFilePath)

xmax2 = 0
ymax2 = 0 
xmin2 = float('inf')
ymin2 = float('inf')
for shape in sf.shapeRecords():
    x2 = np.array([i[0] for i in shape.shape.points[:]])
    y2 = np.array([i[1] for i in shape.shape.points[:]])
    if x2.max() > xmax2:
        xmax2 = x2.max()
    if y2.max() > ymax2:
        ymax2 = y2.max() 
    if x2.min() < xmin2:
        xmin2 = x2.min()
    if y2.min() < ymin2:
        ymin2 = y2.min()
    
l = len(data_locs.drop('time', axis = 1).columns.values) - 1
l2 = len(data_locs)
aspect = 1.5


for j in range(l2):
    weights = np.array(np.meshgrid(np.zeros([N,]), np.zeros([N,]))).prod(0)
    
    x = np.zeros(l)
    y = np.zeros(l)
    z = np.zeros(l)
    
    fig = plt.figure()
    ax = fig.add_subplot()
    
    for shape in sf.shapeRecords():
        x2 = np.array([i[0] for i in shape.shape.points[:]])
        y2 = np.array([i[1] for i in shape.shape.points[:]])
        x2 = ((x2 - xmin2) * (emax - wmax) / (xmax2 - xmin2)) + wmax
        y2 = ((y2 - ymin2) * (nmax - smax) / (ymax2 - ymin2)) + smax
        ax.plot(x2, y2, c = 'grey', lw = 0.5, alpha = 0.4, zorder = 3)
    for i in range(l):
        x[i] = float(list(data_locs.drop('time', axis = 1).columns.values)[i].split()[1].replace(',',''))
        y[i] = float(list(data_locs.drop('time', axis = 1).columns.values)[i].split()[0].replace(',',''))
        z[i] = int(data_locs.iat[j,i+1])
        xgauss = normal_pdf(xx, x[i], 0.00001*aspect)
        ygauss = normal_pdf(yy, y[i], 0.00001)
        weights += z[i]*np.array(np.meshgrid(xgauss, ygauss)).prod(0)

    ax.imshow(weights, extent=(xmin, xmax, ymin, ymax), cmap='hot', origin='lower', vmin=0, vmax=30, zorder=2)
    string_time = str(data_locs.iat[j,0])
    plt.text(17.05, 51.025, string_time, c = 'white', )
    ax.scatter(x, y, c=z/max(z), cmap="hot", s = 3, edgecolors = 'lightgreen', linewidth=0.2, zorder = 10)
    plt.axis('off')
    ax.set_aspect(aspect)
    save_string = 'Pics/pic'+str(j)+'.png'
    plt.savefig(save_string, bbox_inches='tight')
    plt.close('all')

