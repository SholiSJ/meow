from math import radians, cos, sin, asin, sqrt

def distance(): 
    nwlat=float(input('Enter Northwest latitude'))
    nwlong=float(input('Enter Northwest longitude'))
    selat=float(input('Enter Southeast latitude'))
    selong=float(input('Enter Southeast longitude')) 
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(nwlong) 
    lon2 = radians(selong) 
    lat1 = radians(nwlat) 
    lat2 = radians(selat)
    dlon = 0 
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  
    len=c #length
    dlon = lon2 - lon1  
    dlat = 0
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  #breadth
    return(c*len*40589641)
    


print(distance())