# -*- coding: UTF-8 -*-

import io
import json
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator
import csv
import time
import sys
reload (sys)
sys.setdefaultencoding('utf-8')


# read API keys
with io.open('config_secret.json') as cred:
    creds = json.load(cred)
    auth = Oauth1Authenticator(**creds)
    client = Client(auth)
def get_search_parameters(offset):
    params = {
        'term': 'restaurant',
        'lang': 'fr',
        'radius_filter': '40000',
        'sort': '0',
        'offset': '{}'.format(str(offset)),
        'limit': '20'
    }
    return params


locations=['Atlanta','Marietta','Sandy Springs']


bb=[]
cc=[]
csvfile = file('dataset_offset_cities_try.csv', 'wb')
writer = csv.writer(csvfile)
headers=['name','rating','review_count','latitude','longitude','postal_code','menu_data_updated','categories','City','State']
writer.writerow(headers)

for lat in locations:
    print len(bb)
    for k in range(0,980,20):
        params = get_search_parameters(k)
        print params
        aa = client.search(lat, **params)
        print len(aa.businesses)
        s=0
        for j in range(0,len(aa.businesses)):
            if aa.businesses[j].location.coordinate:
                if aa.businesses[j].location.state_code == 'GA':
                    if aa.businesses[j].name not in cc:
                        cc.append(aa.businesses[j].name)
                        bb.append(aa.businesses[j].location.postal_code)
                        writer.writerow([aa.businesses[j].name, aa.businesses[j].rating, aa.businesses[j].review_count,
                                             aa.businesses[j].location.coordinate.latitude,
                                             aa.businesses[j].location.coordinate.longitude, aa.businesses[j].location.postal_code,
                                             aa.businesses[j].menu_date_updated, aa.businesses[j].categories[1],
                                            aa.businesses[j].location.city, aa.businesses[j].location.state_code])
                        time.sleep(0.2)
                        s=s+1
                        print s
                    elif aa.businesses[j].location.postal_code not in bb:
                        cc.append(aa.businesses[j].name)
                        bb.append(aa.businesses[j].location.postal_code)
                        writer.writerow([aa.businesses[j].name, aa.businesses[j].rating, aa.businesses[j].review_count,
                                             aa.businesses[j].location.coordinate.latitude,
                                             aa.businesses[j].location.coordinate.longitude, aa.businesses[j].location.postal_code,
                                             aa.businesses[j].menu_date_updated, aa.businesses[j].categories,
                                        aa.businesses[j].location.city, aa.businesses[j].location.state_code])
                        time.sleep(0.2)
                        s=s+1
                        print s




#csvfile = file('dataset_offset.csv', 'wb')
#writer = csv.writer(csvfile)
#headers=['name','rating','review_count','latitude','longitude','postal_code','menu_data_updated','categories']
#writer.writerow(headers)
#for h in range(0, len(bb) - 1):
#    if bb[h].location.city == "Atlanta":
#        writer.writerow([bb[h].name, bb[h].rating, bb[h].review_count, bb[h].location.coordinate.latitude,
#                         bb[h].location.coordinate.longitude, bb[h].location.postal_code,
#                         bb[h].menu_date_updated, bb[h].categories])
csvfile.close()