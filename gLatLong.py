# DanCo substantially altering this:
# gLatLong.py - M.Keranen (mksql@yahoo.com) - 01/09/2006
# Erica updated to current API
# ------------------------------------------------------
# Get lat/long coordinates of an address from Google Maps

import os,urllib,json,BeautifulSoup, time

def get_coords(addr):
    time.sleep(1.1)
    '''Attempt to resolve an address to an unambiguous geocoded location using Google.
        Return (lat, lon) if Google returns exactly one address; otherwise, return None.
    '''
    # Encode query string into URL
    url = 'http://maps.google.com/?q=' + urllib.quote(addr) + '&output=kml'

    # Original version, based on 2006-era API
    # Get location from KML
    #soup = BeautifulSoup.BeautifulStoneSoup(urllib.urlopen(url).read())
    #print soup
    #if ( not soup.find("latitude") ):
        # error of some kind (network?  ambiguous address?)
        # If I were a real API I'd do better with this.
    #  return None
    #else:
        # Assume one lat, long for one placemark.
    #  lat = soup.find("latitude").contents
    #    lon = soup.find("longitude").contents
    #    return (lat, lon)

    # From the current Google Maps API, we can just get json (and, as a bonus, request
    # unicode data in the return.
    # url = 'http://maps.google.com/maps/geo?q=' + urllib.quote(addr) + '&output=json&oe=utf8'
    url = 'http://maps.googleapis.com/maps/api/geocode/json?address=' + urllib.quote(addr) +'&sensor=false'
    data = json.loads(urllib.urlopen(url).read())
    try:
        # Assumes the first Point (if we get one or more) is the right one.
        # If no points, this means error.
        # If several points, we assume the one that Google thinks is the best match.
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return (lng, lat)
    except:
        return None
    

# Just a little testing.

if __name__ == '__main__':
    addr = raw_input('\nAddress or (Lat,Long): ')
    while addr <> '':
        result = get_coords(addr)
        if ( not result ):
            print "Probably an ambiguous address."
        else:
            print ">>> (%s, %s)\n" % (result)
            addr = raw_input('\nAddress or (Lat,Long): ')
