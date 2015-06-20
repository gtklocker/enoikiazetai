from bs4 import BeautifulSoup
import requests
import re
import gmaps
import geojson

STREET_PATTERN = re.compile(r'(?<=στην οδό\s)([Α-Ωα-ωά-ώ.]*)\s*([Α-Ωα-ωά-ώ0-9 --&.]*?)(?=[,.])', re.UNICODE)
GMAPS_API = gmaps.Geocoding()

def get_street(post):
    match = STREET_PATTERN.search(post)
    if match:
        ret = ''
        if any(c == '&' or c.isdigit() for c in match.group(2)):
            ret = ' '.join(match.groups())
        else:
            ret = match.group(1).replace('.', '')
        return ret.split(' και ', 1)[0].strip()
    return None

def get_coordinates(street):
    obj = GMAPS_API.geocode(street)[0]['geometry']['location']
    return geojson.Point((obj['lng'], obj['lat']))

if __name__ == '__main__':
    features = []
    offset = 0
    while True:
        print("Reading page %d." % offset)
        r = requests.get('http://enoikiazetai.uoi.gr/show.php?offset=%d' % offset)
        r.encoding = 'UTF8'
        b = BeautifulSoup(r.text)
        ads = [x.get_text().strip() for x in b.find_all('div', align='left', class_='smalls')]
        if len(ads) == 0:
            print('Finished.')
            break
        for ad in ads:
            if get_street(ad):
                street = get_street(ad) + ', Ιωάννινα'
                coordinates = get_coordinates(street)

                features.append(geojson.Feature(geometry=coordinates, properties={'ad': ad}))
            else:
                features.append(geojson.Feature(geometry=geojson.Point((20.887282, 39.664420)), properties={'ad': ad}))

        offset += 1

    with open('ads.geojson', 'w') as f:
        f.write(str(geojson.FeatureCollection(features)))
