# Testing simlation of generating random points 
from __future__ import division
import numpy as np
import math
from math import radians, cos, sin, asin, sqrt
import bearing

def create_random_point(x0,y0,distance):
    """
            Utility method for simulation of the points
    """   
    r = distance/ 111300
    u = np.random.uniform(0,1)
    v = np.random.uniform(0,1)
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    x1 = x / np.cos(y0)
    y = w * np.sin(t)
    return (x0+x1, y0 +y)


latitude1,longitude1 = 36.653205, -121.797626 
points = []

# for i in range(0,5):
#     # print i
#     points.append(create_random_point(latitude1,longitude1 ,100 ))
    # x,y = create_random_point(latitude1,longitude1 ,100 )
    # dist = bearing.haversine(x,y,latitude1,longitude1)
    # print "geocoords: " + str(x) + ", " + str(y)
    # print "Distance between points is " ,dist    # a value approxiamtely less than 100 meters   


# for i in range(0,5):
#     print i
#     x,y = points[i]
    # dist = bearing.haversine(x,y, latitude1, longitude1)
    # print "geocoords: " + str(x) + ", " + str(y)
    # print "Distance between points is " ,dist    # a value approxiamtely less than 100 meters   

# redo = False
# bad = False
# count = 0

# while (redo == False):
#     print "NUMBER " + str(count)
#     for i in range(0, 5):
#         print "i " + str(i)
#         testCoordX, testCoordY = points[i]
#         for j in range(i + 1, 5):
#             print "j " + str(j)
#             x,y = points[j]
#             dist = bearing.haversine(x,y, testCoordX, testCoordY)
#             if (dist < 1):
#                 bad = True
#                 print testCoordX, testCoordY
#                 print x,y
#                 print "Bad distance between points is " ,dist    # a value approxiamtely less than 100 meters 
#                 points[j] = x + 0.00000162145, y + 0.1
#                 break
#             else:
#                 print "Distance between points is " ,dist    # a value approxiamtely less than 100 meters 
#         if (bad == True):
#             bad = False
#             break
#         if (i == 4 and bad == False):
#             redo = True;
#     count += 1
#     if (count > 2):
#         redo = True
#         print "limit"
    
# for i in range(0,5):
#     print i
#     x,y = points[i]
#     dist = bearing.haversine(x,y, latitude1, longitude1)
#     print "geocoords: " + str(x) + ", " + str(y)
#     print "Distance between points is " ,dist    # a value approxiamtely less than 100 meters   
