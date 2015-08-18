
import urllib2
import urllib
import json
import time

"""from FG: https://github.com/fgassert/agol_util"""


OD_GROUP_IDS = {
    "managed forests": "460c7c785daf40cf9a776d251792bef1",
    "mining": "7a741c91c1254468ba647792dabc3057",
    "oil palm": "7efb7a9499ef4138a997a4b5db36d04d",
    "resource rights": "fa6a7bf23f7d45d3a9f97b48fac15e85",
    "Wood Fiber Plantations": "be04478fe3414371ab61c8063d30e770",
    "Conservation": "9b895183c97d420995b87ef714d20f50",
    "Forest cover": "577b964b7d8b41b9822d39a7be261bff",
    "Land Rights": "30958b493339437f835d49660b0d92de"
}


AGOL_BASE_URL = "http://gfw.maps.arcgis.com/home/group.html?id=%s"

def test_this_shit():
    # Create an instance of AGOL
    # 
    res = agol.add_shapefile_from_url('http://data.wri.org/Aqueduct/aqueduct_global_dl_shp2.zip')


class AGOL_util:
    """
    Minimal client library for ArcGIS online API
    
    Parameters:
    root_url: portal root rest url e.g. http://myorg.arcgis.com/sharing/rest
    username: valid arggis online username
    password: valid arggis online password
    """
    
    def __init__(self, root_url, username, password):
        self.url = root_url
        self._check_items = []
        self._uid = username
        self._pwdd = password
        self._validate_user(username, password)

    def _validate_user(self, username, password):
        '''
        Requests token based on username and password
        no error catching
        '''
        keys = {'username':username,
                'password':password,
                'referer':self.url,
                'f':'json'}
        data = urllib.urlencode(keys)
        req = urllib2.Request('https://www.arcgis.com/sharing/rest/generateToken', data)
        resp = json.load(urllib2.urlopen(req))
        if 'token' in resp:
            self._token = resp['token']
            self._expiry = resp['expires']
        else:
            self._token = ''
            self._expiry = 0
        return resp
        
    def get_token(self, nd=False):
        """ 
        returns valid token or false on failure 
        """
        if self._token=='' or self._expiry <= time.time():
            if nd:
                return False
            else:
                self._validate_user(self._uid, self._pwd)
                return(self.get_token(1))
        return self._token
    
    def query(self, endpoint, options):
        '''
        POST to url endpoint with options as data
        autoappends token and json response parameters
        concatinates self.url and endpoind assuming matching /'s

        return as JSON
        '''
        options['token'] = self.get_token()
        options['f'] = 'json'
        data = urllib.urlencode(options)
        requrl = "{}{}".format(self.url, endpoint)
        req = urllib2.Request(requrl, data)
        return json.load(urllib2.urlopen(req))
    
    def add_item_from_url(self, url, options={}):
        options['dataUrl'] = url
        options['async'] = 'true'
        options['overwrite'] = 'true'
        return self.query('/content/users/{}/addItem'.format(self._uid), options)
    def add_shapefile_from_url(self, url, options={}):
        """ URL should point to zipped shapefile """
        options['type'] = 'Shapefile'
        return self.add_item_from_url(url, options)
    
    def get_item_status(self, itemId):
        url = '/content/users/{}/items/{}/status'.format(self._uid, itemId)
        return self.query(url, {})

    def wait_for_completion(self, itemId, timeout=60):
        ''' 
        Check every second for item status to return completed
        
        Return:
        true on completion
        false on timeout or error
        '''
        res = self.get_item_status(itemId)
        t = 0
        while 'status' in res and t < timeout:
            if res['status'] == 'completed':
                return True
            t += 1
            time.sleep(1)
            res = self.get_item_status(itemId)
        return False
    
    def update_item(self, itemId, options):
        url = '/content/users/{}/items/{}/update'.format(self._uid, itemId)
        return self.query(url, options)

    def share_items(self, items, everyone=None, org=None, groups=None):
        """ shares items defined by item ids with given groups, org, or everyone """
        options = {}
        if groups is not None:
            options['groups'] = groups
        if everyone is not None:
            options['everyone'] = everyone
        if org is not None:
            options['org'] = org
        if type(items) == list:
            items = ','.join(items)
        options['items'] = items
        return self.query('/content/users/{}/shareItems'.format(self._uid), options)

    def publish_item(self, itemId, options, publishParameters):
        options['itemID'] = itemId
        options['publishParameters'] = json.dumps(publishParameters)
        options['overwrite'] = 'true'
        return self.query('/content/users/{}/publish'.format(self._uid), options)
    def publish_shapefile(self, itemId, options={}, publishParameters={}):
        options['fileType'] = 'shapefile'
        if 'name' not in publishParameters:
            publishParameters['name'] = itemId
        return self.publish_item(itemId, options, publishParameters)

    def delete_item(self, itemId):
        url = '/content/users/{}/items/{}/delete'.format(self._uid, itemId)
        return self.query(url)