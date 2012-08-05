#!/usr/bin/env python
import requests
import json

class Sincerely:
    def __init__(self, url_base, app_key):
        self.url_base = url_base
        self.app_key = app_key

    def upload(self, path):
        """ Upload an image file and return an id """
        contents = open(path, 'rb').read().encode('base64')
        files = {'photo': open(path, 'rb')}
        resp = requests.post('%s/%s' % (self.url_base, 'upload'),
                data={'appkey': self.app_key}, files=files)

        result = json.loads(resp.text)
        print result
        if result['success'] == True:
            return result['id']

    def create(self, photo_id, user_info, message):
        """ Create a postcard based on the photo id and user info """
        data = {
            'message': message,
            'frontPhotoId': photo_id,
            'recipients': json.dumps([{
                'id': 123,
                'name': user_info['name'],
                'street1': user_info['street1'],
                'street2': user_info['street2'],
                'city': user_info['city'],
                'state': user_info['state'],
                'postalcode': user_info['zip'],
                'country': user_info['country']
            }]),
            'sender': json.dumps({
                'name': 'eCommerce Hack Day Team',
                'email': 'graham@burritobowl.com',
                'street1': '618 Rodman St',
                'city': 'Philadelphia',
                'state': 'PA',
                'postalcode': '19147',
                'country': 'USA'
            }),
            'appkey': self.app_key
        }

        res = requests.post('%s/%s' % (self.url_base, 'create'),
                data=data)

        return json.loads(res.text)['id']

if __name__ == '__main__':
    client = Sincerely(
            'https://snapi.sincerely.com/shiplib',
            'NO214GGXD1PL1F44RZ4MPRWA8WX9SVIXOMATF51P')

    #client = Sincerely(
    #        'http://localhost:8080',
    #        'NO214GGXD1PL1F44RZ4MPRWA8WX9SVIXOMATF51P')
    
    #upload_id = client.upload('/home/graham/Projects/personal/canvas-3x3.jpg')
    upload_id = 10667016
    client.create(upload_id, {
        'name': 'Graham',
        'street1': '618 Rodman St',
        'street2': None,
        'city': 'Philadelphia',
        'state': 'PA',
        'zip': '19147',
        'country': 'United States'
    }, "Hello world!")
