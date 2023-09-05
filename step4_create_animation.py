# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 20:11:31 2023

@author: sfelc
"""

import cv2

frameSize = (1464, 1168)

out = cv2.VideoWriter('output_video.avi',cv2.VideoWriter_fourcc(*'DIVX'), 5, frameSize)

for i in range(352):
    filename = 'Pics/pic'+str(i)+'.png'
    img = cv2.imread(filename)
    out.write(img)

out.release()