import hashlib
import inspect
import json
import oauth2
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

class SocialBase(object):

    def __init__(self, id=None):
        self.id = id

    def _get_id(self, id):
        id = id or self.id

        if not id:
            raise ValueError('Missing or invalid id.')

        return id

class Shares(SocialBase):

    def __init__(self, id=None, fb_token=None):
        SocialBase.__init__(self, id)
        self.fb_token = fb_token

    def buffer(self, id=None):
        id = self._get_id(id)
        res = unirest.get('https://api.bufferapp.com/1/links/shares.json?url=%s' % id)

        if res.code != 200:
            return None

        return { 'count': res.body.get('shares', 0), 'id': id, 'service': this() }

    def delicious(self, id=None):
        id = self._get_id(id)

        # FIX-ME: Not working?
        # res = unirest.get('http://feeds.delicious.com/v2/json/urlinfo/data?url=%s' % id)
        # if res.code != 200:
        #     return None
        # r = res.body[0] if len(res.body) > 0 else {}
        # return { 'count': r.get('total_posts', 0), 'id': id, 'service': this() }

        res = unirest.get('https://avosapi.delicious.com/api/v1/posts/md5/%s' % hashlib.md5(id).hexdigest())

        if res.code != 200:
            return None

        r = res.body.get('pkg', [{}])

        # Invalid URL returns None.
        if r is None:
            r = {}
        else:
            r = r[0]

        return { 'count': r.get('num_saves', 0), 'id': id, 'service': this() }

    def facebook(self, id=None):
        id = self._get_id(id)

        res = unirest.get('https://graph.facebook.com/v2.2/?access_token=%s&id=%s' % (self.fb_token, id))

        if res.code != 200:
            return None

        return { 'count': res.body.get('share', {}).get('share_count', 0), 'id': res.body.get('id', id), 'service': this() }

    def google_plus(self, id=None):
        id = self._get_id(id)
        data = [{ 'method' : 'pos.plusones.get',
                  'id' : 'p',
                  'params': { 'nolog' : True,
                              'id' : id,
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

        return { 'count': parse_int(r.get('metadata', {}).get('globalCounts', {}).get('count', 0)), 'id': r.get('id', id), 'service': this() }

    def linkedin(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://www.linkedin.com/countserv/count/share?url=%s' % id)

        if res.code != 200:
            return 0

        r = parse_jsonp(res.body)

        return { 'count': r.get('count', 0), 'id': r.get('url', id), 'service': this() }

    def pinterest(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://api.pinterest.com/v1/urls/count.json?callback=www&url=%s' % id)

        if res.code != 200:
            return None

        r = parse_jsonp(res.body)

        return { 'count': r.get('count', 0), 'id': r.get('url', id), 'service': this() }

    def pocket(self, id=None):
        id = self._get_id(id)
        res = unirest.get('https://widgets.getpocket.com/v1/button?align=center&count=vertical&label=pocket&url=%s' % id)

        if res.code != 200:
            return None

        html = res.raw_body
        soup = BeautifulSoup(html)
        cnt = soup.find(id="cnt")

        return { 'count': parse_int(cnt.text), 'id': id, 'service': this() }

    def reddit(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://www.reddit.com/api/info.json?url=%s' % id)

        if res.code != 200:
            return None

        infos = res.body.get('data', {}).get('children', [])

        return { 'count': len(infos), 'id': id, 'service': this() }

    def stumbleupon(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://www.stumbleupon.com/services/1.01/badge.getinfo?url=%s' % id)

        if res.code != 200:
            return None

        r = res.body.get('result', {})

        return { 'count': r.get('views', 0), 'id': r.get('url', id), 'service': this() }

    def twitter(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://cdn.api.twitter.com/1/urls/count.json?url=%s' % id)

        if res.code != 200:
            return None

        return { 'count': res.body.get('count', 0), 'id': res.body.get('url', id), 'service': this() }

    def vkontakte(self, id=None):
        id = self._get_id(id)
        res = unirest.get('https://vk.com/share.php?act=count&url=%s' % id)

        if res.code != 200:
            return None

        m = re.match('VK.Share.count\([0-9]+, (?P<count>[0-9]+)\);', res.body)

        if m:
            count = parse_int(m.group('count'))
        else:
            count = 0

        return { 'count': count, 'id': id, 'service': this() }

class Followers(SocialBase):

    def __init__(self, id=None, gplus_key=None, sc_key=None, twitter_auth=None):
        SocialBase.__init__(self, id)
        self.gplus_key = gplus_key
        self.sc_key = sc_key
        self.twitter_auth = twitter_auth or {}

    def google_plus(self, id=None):
        id = self._get_id(id)

        res = unirest.get('https://www.googleapis.com/plus/v1/people/%s?key=%s' % (id, self.gplus_key))

        if res.code != 200:
            return None

        count = res.body.get('plusOneCount', 0) or res.body.get('circledByCount', 0)

        return { 'count': count, 'id': res.body.get('url', id), 'service': this() }

    def soundcloud(self, id=None):
        id = self._get_id(id)

        res = unirest.get('https://api.soundcloud.com/users/%s.json?consumer_key=%s' % (id, self.sc_key))

        if res.code != 200:
            return None

        return { 'count': res.body.get('followers_count', 0), 'id': res.body.get('permalink_url', id), 'service': this() }

    def twitter(self, id=None):
        id = self._get_id(id)

        consumer = oauth2.Consumer(key=self.twitter_auth.get('api_key', ''), secret=self.twitter_auth.get('api_secret', ''))
        token = oauth2.Token(key=self.twitter_auth.get('token_key', ''), secret=self.twitter_auth.get('token_secret', ''))
        client = oauth2.Client(consumer, token)
        res, body = client.request('https://api.twitter.com/1.1/users/lookup.json?screen_name=%s' % id, method='GET')

        if res.get('status') == '200':
            r = json.loads(body)[0]
            id = 'https://twitter.com/%s' % r.get('screen_name', id)
            return { 'count': r.get('followers_count', 0), 'id': id, 'service': this() }
        else:
            return None

class Counter(SocialBase):

    def __init__(self, id=None):
        SocialBase.__init__(self, id)

    def reddit(self, id=None):
        id = self._get_id(id)
        res = unirest.get('http://www.reddit.com/api/info.json?url=%s' % id)

        if res.code != 200:
            return None

        infos = res.body.get('data', {}).get('children', [])

        ups = downs = score = 0

        for i in infos:
            data = i.get('data', {})
            ups += data.get('ups', 0)
            downs += data.get('downs', 0)
            score += data.get('score')

        return { 'shares': len(infos), 'ups': ups, 'downs': downs, 'score': score, 'id': id, 'service': this() }

    def youtube(self, id=None):
        id = self._get_id(id)

        if '?' in id:
            query = id[id.find('?') + 1:]
            params = query.split('&')

            for p in params:
                v = p.split('=')

                if len(v)== 2 and v[0] == 'v':
                    id = v[1]
                    break

        res = unirest.get('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % id)

        if res.code != 200:
            return None

        r = res.body.get('entry', {})

        return { 'views': r.get('yt$statistics', {}).get('viewCount', 0),
                 'likes': r.get('yt$rating', {}).get('numLikes', 0),
                 'dislikes': r.get('yt$rating', {}).get('numDislikes', 0),
                 'favorites': r.get('yt$statistics', {}).get('favoriteCount', 0),
                 'id': 'https://www.youtube.com/v/%s' % id,
                 'service': this() }


if __name__ == '__main__':
    import os

    fb_token = os.environ.get('FB_TOKEN', '')
    gplus_key = os.environ.get('GPLUS_KEY', '')
    sc_key = os.environ.get('SOUNDCLOUD_KEY', '')
    twitter_auth = {
        'api_key': os.environ.get('TWITTER_API_KEY', ''),
        'api_secret': os.environ.get('TWITTER_API_SECRET', ''),
        'token_key': os.environ.get('TWITTER_TOKEN_KEY', ''),
        'token_secret': os.environ.get('TWITTER_TOKEN_SECRET', ''),
    }

    S = Shares('https://www.youtube.com/watch?v=9bZkp7q19f0', fb_token=fb_token)
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

    F = Followers(gplus_key=gplus_key, sc_key=sc_key, twitter_auth=twitter_auth)
    print('G+ = %s' % F.google_plus('+google'))
    print('SoundCloud = %s' % F.soundcloud('soundcloud'))
    print('Twitter = %s' % F.twitter('twitter'))

    C = Counter('https://www.youtube.com/watch?v=9bZkp7q19f0')
    print('Reddit = %s' % C.reddit())
    print('YouTube = %s' % C.youtube())