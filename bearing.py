import math
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
  R = 6372.795477598  # radius of the earth in km
  x = (lon2 - lon1) * cos( 0.5*(lat2+lat1) )
  y = lat2 - lat1
  d = R * sqrt( x*x + y*y )
  return d

def bearing(sLat, sLng, eLat, eLng):
    startLat = math.radians(sLat)
    startLong = math.radians(sLng)
    endLat = math.radians(eLat)
    endLong = math.radians(eLng)
    
    dLong = endLong - startLong
    
    dPhi = math.log(math.tan(endLat/2.0+math.pi/4.0)/math.tan(startLat/2.0+math.pi/4.0))
    if abs(dLong) > math.pi:
         if dLong > 0.0:
             dLong = -(2.0 * math.pi - dLong)
         else:
             dLong = (2.0 * math.pi + dLong)
    
    bearing = (math.degrees(math.atan2(dLong, dPhi)) + 360.0) % 360.0;
    
    print(bearing)
    
    return bearing

# print str(haversine(startLong, startLat, endLong, endLat)) + " km"