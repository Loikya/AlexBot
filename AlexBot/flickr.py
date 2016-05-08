import flickrapi
import os
import sys
import random
api_key = "f65ecb65aba7cfc667b32b464af5e4b2"
secret="caf4d6568c0d7e4b"
url_template = 'http://farm%(farm_id)s.staticflickr.com/%(server_id)s/%(photo_id)s_%(secret)s.jpg'

def url_for_photo(p):
    return url_template % {
        'server_id': p.get('server'),
        'farm_id': p.get('farm'),
        'photo_id': p.get('id'),
        'secret': p.get('secret'),
    }
    
def get_random_img(word):
    flickr = flickrapi.FlickrAPI(api_key, secret)
    return url_for_photo(random.choice(flickr.photos_search(tags=word, per_page=20)[0]))
