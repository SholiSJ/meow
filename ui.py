import requests
from io import BytesIO
from math import log, exp, tan, atan, ceil
from PIL import Image
import sys
from math import radians, cos, sin, asin, sqrt
import numpy 
import math
import cv2

# circumference/radius
tau = 6.283185307179586
# One degree in radians, i.e. in the units the machine uses to store angle,
# which is always radians. For converting to and from degrees. See code for
# usage demonstration.
DEGREE = tau/360

ZOOM_OFFSET = 8
GOOGLE_MAPS_API_KEY = 'AIzaSyDpe69nVjN1FZ6y4unn3e4PY_wGO7bpL4M'  # set to 'your_API_key'

# Max width or height of a single image grabbed from Google.
MAXSIZE = 640
# For cutting off the logos at the bottom of each of the grabbed images.  The
# logo height in pixels is assumed to be less than this amount.
LOGO_CUTOFF = 32

def area(): 
    lon1 = radians(nwlong) 
    lon2 = radians(selong) 
    lat1 = radians(nwlat) 
    lat2 = radians(selat)
    dlon = 0 
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2 #haversine
    c = 2 * asin(sqrt(a))  
    len=c #length
    dlon = lon2 - lon1  
    dlat = 0
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))  #breadth
    print('area of land between coordinates :{}Km sqaure'.format(round(c*len*40589641,3)))

def psnr(img1, img2):
    mse = numpy.mean( (img1 - img2) ** 2 )
    if mse == 0:
        return 100
    PIXEL_MAX = 255.0
    return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))
    

def latlon2pixels(lat, lon, zoom):
    mx = lon
    my = log(tan((lat + tau/4)/2))
    res = 2**(zoom + ZOOM_OFFSET) / tau
    px = mx*res
    py = my*res
    return px, py

def pixels2latlon(px, py, zoom):
    res = 2**(zoom + ZOOM_OFFSET) / tau
    mx = px/res
    my = py/res
    lon = mx
    lat = 2*atan(exp(my)) - tau/4
    return lat, lon


def get_maps_image(NW_lat_long, SE_lat_long, zoom=18):

    ullat, ullon = NW_lat_long
    lrlat, lrlon = SE_lat_long

    # convert all these coordinates to pixels
    ulx, uly = latlon2pixels(ullat, ullon, zoom)
    lrx, lry = latlon2pixels(lrlat, lrlon, zoom)
  

    # calculate total pixel dimensions of final image
    dx, dy = lrx - ulx, uly - lry
    # calculate rows and columns
    cols, rows = ceil(dx/MAXSIZE), ceil(dy/MAXSIZE)

    # calculate pixel dimensions of each small image
    width = ceil(dx/cols)
    height = ceil(dy/rows)
    heightplus = height + LOGO_CUTOFF

    # assemble the image from stitched
    final = Image.new('RGB', (int(dx), int(dy)))
    for x in range(cols):
        for y in range(rows):
            dxn = width * (0.5 + x)
            dyn = height * (0.5 + y)
            latn, lonn = pixels2latlon(
                    ulx + dxn, uly - dyn - LOGO_CUTOFF/2, zoom)
            position = ','.join((str(latn/DEGREE), str(lonn/DEGREE)))
            print(x, y, position)
            urlparams = {
                    'center': position,
                    'zoom': str(zoom),
                    'size': '%dx%d' % (width, heightplus),
                    'maptype': 'satellite',
                    'sensor': 'false',
                    'scale': 1
                }
            if GOOGLE_MAPS_API_KEY is not None:
                urlparams['key'] = GOOGLE_MAPS_API_KEY

            url = 'http://maps.google.com/maps/api/staticmap'
            try:                  
                response = requests.get(url, params=urlparams)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(e)
                sys.exit(1)

            im = Image.open(BytesIO(response.content))                  
            final.paste(im, (int(x*width), int(y*height)))


    return final

if __name__ == '__main__':
    nwlat=float(input('Enter Northwest latitude:'))
    nwlong=float(input('Enter Northwest longitude:'))
    selat=float(input('Enter Southeast latitude:'))
    selong=float(input('Enter Southeast longitude:'))

    if((nwlat<=selat)or(selong<=nwlong)):
        print('wrong coordinates')
        exit(1)
    else :
        area()

    NW_lat_long =(nwlat*DEGREE,nwlong*DEGREE)
    SE_lat_long =(selat*DEGREE,selong*DEGREE)


    zoom = 18  # be careful not to get too many images!

    result = get_maps_image(NW_lat_long, SE_lat_long, zoom=18)
    result.show()
    result.save('map.png')
    im = Image.open("map.png")
    rgb_im = im.convert('RGB')
    rgb_im.save('map.jpg')
    original = cv2.imread("a.jpg",0)
    new = cv2.imread("b.jpg",0)
    Imagesimilarity=psnr(original,new)
    if(Imagesimilarity==100):
        print('no difference in images')
    else:
        print('difference in image detected')
        
