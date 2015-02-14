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

class Counter(object):

    def __init__(self, url=None):
        self.url = url

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

        return { 'shares': res.body.get('shares', 0), 'url': url, 'service': this() }

    def delicious(self, url=None):
        url = self._get_url(url)

        # FIX-ME: Not working?
        # res = unirest.get('http://feeds.delicious.com/v2/json/urlinfo/data?url=%s' % url)
        # if res.code != 200:
        #     return None
        # r = res.body[0] if len(res.body) > 0 else {}
        # return { 'shares': r.get('total_posts', 0), 'url': url, 'service': this() }

        res = unirest.get('https://avosapi.delicious.com/api/v1/posts/md5/%s' % hashlib.md5(url).hexdigest())

        if res.code != 200:
            return None

        r = res.body.get('pkg', [{}])

        # Invalid URL returns None.
        if r is None:
            r = {}
        else:
            r = r[0]

        return { 'shares': r.get('num_saves', 0), 'url': url, 'service': this() }

    def digg(self, url=None):
        # TODO: implement
        return None

    def facebook(self, url=None):
        url = self._get_url(url)

        # FIX-ME: This api is deprecated.
        # 'http://graph.facebook.com/?id=' + url
        # 'https://api.facebook.com/method/fql.query?query=' + encode( "SELECT total_count, url FROM link_stat WHERE url='" + url + "'" ) + '&format=json&callback=' );
        res = unirest.get('http://api.facebook.com/restserver.php?method=links.getStats&urls=%s&format=json' % url)

        if res.code != 200:
            return None

        r = res.body[0]

        return { 'shares': r.get('share_count', 0), 'likes': r.get('like_count', 0), 'url': r.get('url', url), 'service': this() }

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

        return { 'shares': r.get('metadata', {}).get('globalCounts', {}).get('count', 0), 'url': r.get('id', url), 'service': 'g+' }

    def linkedin(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.linkedin.com/countserv/count/share?url=%s' % url)

        if res.code != 200:
            return 0

        r = parse_jsonp(res.body)

        return { 'shares': r.get('count', 0), 'url': r.get('url', url), 'service': this() }

    def pinterest(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://api.pinterest.com/v1/urls/count.json?callback=www&url=%s' % url)

        if res.code != 200:
            return None

        r = parse_jsonp(res.body)

        return { 'shares': r.get('count', 0), 'url': r.get('url', url), 'service': this() }

    def pocket(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://widgets.getpocket.com/v1/button?align=center&count=vertical&label=pocket&url=%s' % url)

        if res.code != 200:
            return None

        html = res.raw_body
        soup = BeautifulSoup(html)
        cnt = soup.find(id="cnt")

        return { 'count': cnt.text, 'url': url, 'service': this() }

    def reddit(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.reddit.com/api/info.json?url=%s' % url)

        if res.code != 200:
            return None

        infos = res.body.get('data', {}).get('children', [])

        ups = downs = score = 0

        for i in infos:
            data = i.get('data', {})
            ups += data.get('ups', 0)
            downs += data.get('downs', 0)
            score += data.get('score')

        return { 'ups' : ups, 'downs' : downs, 'score' : score, 'url': url, 'service': this() }

    def stumbleupon(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.stumbleupon.com/services/1.01/badge.getinfo?url=%s' % url)

        if res.code != 200:
            return None

        r = res.body.get('result', {})

        return { 'views': r.get('views', 0), 'url': r.get('url', url), 'service': this() }

    def twitter(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://cdn.api.twitter.com/1/urls/count.json?url=%s' % url)

        if res.code != 200:
            return None

        return { 'shares': res.body.get('count', 0), 'url': res.body.get('url', url), 'service': this() }

    def tumblr(self, url=None):
        # TODO: implement
        return None

    def vkontakte(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://vk.com/share.php?act=count&url=%s' % url)

        if res.code != 200:
            return None

        m = re.match('VK.Share.count\([0-9]+, (?P<count>[0-9]+)\);', res.body)

        if m:
            count = m.group('count')
        else:
            count = 0

        return { 'count': count, 'url': url, 'service': this() }

    def youtube(self, url=None):
        url = self._get_url(url)

        if '?' in url:
            query = url = url[url.find('?') + 1:]
            params = query.split('&')

            for p in params:
                v = p.split('=')

                if len(v)== 2 and v[0] == 'v':
                    url = v[1]
                    break

        res = unirest.get('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % url)

        if res.code != 200:
            return None

        r = res.body.get('entry', {})

        return { 'views': r.get('yt$statistics', {}).get('viewCount', 0),
                 'likes': r.get('yt$rating', {}).get('numLikes', 0),
                 'dislikes': r.get('yt$rating', {}).get('numDislikes', 0),
                 'url': 'https://www.youtube.com/v/%s' % url,
                 'service': this() }

if __name__ == '__main__':
    C = Counter('https://www.youtube.com/watch?v=9bZkp7q19f0')
    print('Buffer = %s' % C.buffer())
    print('Delicious = %s' % C.delicious())
    print('Facebook = %s' % C.facebook())
    print('G+ = %s' % C.google_plus())
    print('Linkedin = %s' % C.linkedin())
    print('Pinterest = %s' % C.pinterest())
    print('Pocket = %s' % C.pocket())
    print('Reddit = %s' % C.reddit())
    print('StumbleUpon = %s' % C.stumbleupon())
    print('Twitter = %s' % C.twitter())
    print('VK = %s' % C.vkontakte())
    print('YouTube = %s' % C.youtube())