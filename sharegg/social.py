import hashlib
import inspect
import json
import re
import unirest

from bs4 import BeautifulSoup

this = lambda: inspect.stack()[1][3]

def parse_jsonp(jsonp):
    x, y = jsonp.index('(') + 1, jsonp.rindex(')')
    return json.loads(jsonp[x:y])

def parse_int(num):
    if type(num) in [str, unicode]:
        return int(num) if num.isdigit() else 0

    return int(num)

class Shares(object):

    def __init__(self, url=None, fb_token=None):
        self.url = url
        self.fb_token = fb_token

    def _get_url(self, url):
        url = url or self.url

        if not url:
            raise ValueError('Missing or invalid url.')

        return url

    def buffer(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://api.bufferapp.com/1/links/shares.json?url=%s' % url)

        if res.code != 200:
            return None

        return { 'count': res.body.get('shares', 0), 'url': url, 'service': this() }

    def delicious(self, url=None):
        url = self._get_url(url)

        # FIX-ME: Not working?
        # res = unirest.get('http://feeds.delicious.com/v2/json/urlinfo/data?url=%s' % url)
        # if res.code != 200:
        #     return None
        # r = res.body[0] if len(res.body) > 0 else {}
        # return { 'count': r.get('total_posts', 0), 'url': url, 'service': this() }

        res = unirest.get('https://avosapi.delicious.com/api/v1/posts/md5/%s' % hashlib.md5(url).hexdigest())

        if res.code != 200:
            return None

        r = res.body.get('pkg', [{}])

        # Invalid URL returns None.
        if r is None:
            r = {}
        else:
            r = r[0]

        return { 'count': r.get('num_saves', 0), 'url': url, 'service': this() }

    def facebook(self, url=None):
        url = self._get_url(url)

        res = unirest.get('https://graph.facebook.com/v2.2/?access_token=%s&id=%s' % (self.fb_token, url))

        if res.code != 200:
            return None

        return { 'count': res.body.get('share', {}).get('share_count', 0), 'url': res.body.get('id', url), 'service': this() }

    def google_plus(self, url=None):
        url = self._get_url(url)
        data = [{ 'method' : 'pos.plusones.get',
                  'id' : 'p',
                  'params': { 'nolog' : True,
                              'id' : url,
                              'source' : 'widget',
                              'userId' : '@viewer',
                              'groupId' : '@self' },
                   'jsonrpc' : '2.0',
                   'key' : 'p',
                   'apiVersion' : 'v1' }]

        res = unirest.post('https://clients6.google.com/rpc?key=AIzaSyCKSbrvQasunBoV16zDH9R33D88CeLr9gQ',
                           headers={ "Accept": "application/json", "Content-Type": "application/json" },
                           params=json.dumps(data))

        if res.code != 200 or len(res.body) < 1:
            return None

        r = res.body[0].get('result', {})

        return { 'count': parse_int(r.get('metadata', {}).get('globalCounts', {}).get('count', 0)), 'url': r.get('id', url), 'service': this() }

    def linkedin(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.linkedin.com/countserv/count/share?url=%s' % url)

        if res.code != 200:
            return 0

        r = parse_jsonp(res.body)

        return { 'count': r.get('count', 0), 'url': r.get('url', url), 'service': this() }

    def pinterest(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://api.pinterest.com/v1/urls/count.json?callback=www&url=%s' % url)

        if res.code != 200:
            return None

        r = parse_jsonp(res.body)

        return { 'count': r.get('count', 0), 'url': r.get('url', url), 'service': this() }

    def pocket(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://widgets.getpocket.com/v1/button?align=center&count=vertical&label=pocket&url=%s' % url)

        if res.code != 200:
            return None

        html = res.raw_body
        soup = BeautifulSoup(html)
        cnt = soup.find(id="cnt")

        return { 'count': parse_int(cnt.text), 'url': url, 'service': this() }

    def reddit(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.reddit.com/api/info.json?url=%s' % url)

        if res.code != 200:
            return None

        infos = res.body.get('data', {}).get('children', [])

        return { 'count' : len(infos), 'url': url, 'service': this() }

    def stumbleupon(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.stumbleupon.com/services/1.01/badge.getinfo?url=%s' % url)

        if res.code != 200:
            return None

        r = res.body.get('result', {})

        return { 'count': r.get('views', 0), 'url': r.get('url', url), 'service': this() }

    def twitter(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://cdn.api.twitter.com/1/urls/count.json?url=%s' % url)

        if res.code != 200:
            return None

        return { 'count': res.body.get('count', 0), 'url': res.body.get('url', url), 'service': this() }

    def vkontakte(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://vk.com/share.php?act=count&url=%s' % url)

        if res.code != 200:
            return None

        m = re.match('VK.Share.count\([0-9]+, (?P<count>[0-9]+)\);', res.body)

        if m:
            count = parse_int(m.group('count'))
        else:
            count = 0

        return { 'count': count, 'url': url, 'service': this() }

if __name__ == '__main__':
    import os

    S = Shares('https://www.youtube.com/watch?v=9bZkp7q19f0', os.environ.get('FB_TOKEN', ''))
    print('Buffer = %s' % S.buffer())
    print('Delicious = %s' % S.delicious())
    print('Facebook = %s' % S.facebook())
    print('G+ = %s' % S.google_plus())
    print('Linkedin = %s' % S.linkedin())
    print('Pinterest = %s' % S.pinterest())
    print('Pocket = %s' % S.pocket())
    print('Reddit = %s' % S.reddit())
    print('StumbleUpon = %s' % S.stumbleupon())
    print('Twitter = %s' % S.twitter())
    print('VK = %s' % S.vkontakte())