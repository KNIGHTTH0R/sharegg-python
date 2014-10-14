import inspect
import json
import unirest

_this = lambda: inspect.stack()[1][3]

def _parse_jsonp(jsonp):
    x, y = jsonp.index('(') + 1, jsonp.rindex(')')
    return json.loads(jsonp[x:y])

class StatsCounter(object):

    def __init__(self, url):
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

        return { 'shares': res.body.get('count', 0), 'url': url, 'provider': _this() }

    def delicious(self, url=None):
        # FIX-ME: Not working?
        url = self._get_url(url)

        res = unirest.get('http://feeds.delicious.com/v2/json/urlinfo/data?url=%s' % url)

        if res.code != 200:
            return None

        r = res.body[0] if len(res.body) > 0 else {}

        return { 'shares': r.get('total_posts', 0), 'url': url, 'provider': _this() }

    def digg(self, url=None):
        # TODO: implement
        return None

    def facebook(self, url=None):
        url = self._get_url(url)

        # FIX-ME: This api is deprecated.
        # 'https://api.facebook.com/method/fql.query?query=' + encode( "SELECT total_count, url FROM link_stat WHERE url='" + url + "'" ) + '&format=json&callback=' );
        res = unirest.get('http://api.facebook.com/restserver.php?method=links.getStats&urls=%s&format=json' % url)

        if res.code != 200:
            return None

        r = res.body[0]

        return { 'shares': r.get('share_count', 0), 'likes': r.get('like_count', 0), 'url': r.get('url', url), 'provider': _this() }

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

        return { 'shares': r.get('metadata', {}).get('globalCounts', {}).get('count', 0), 'url': r.get('id', url), 'provider': 'g+' }

    def linkedin(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.linkedin.com/countserv/count/share?url=%s' % url)

        if res.code != 200:
            return 0

        r = _parse_jsonp(res.body)

        return { 'shares': r.get('count', 0), 'url': r.get('url', url), 'provider': _this() }

    def pinterest(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://api.pinterest.com/v1/urls/count.json?callback=www&url=%s' % url)

        if res.code != 200:
            return None

        r = _parse_jsonp(res.body)

        return { 'shares': r.get('count', 0), 'url': r.get('url', url), 'provider': _this() }

    def pocket(self, url=None):
        # TODO: implement
        return None

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

        return { 'ups' : ups, 'downs' : downs, 'score' : score, 'url': url, 'provider': _this() }

    def stumbleupon(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://www.stumbleupon.com/services/1.01/badge.getinfo?url=%s' % url)

        if res.code != 200:
            return None

        r = res.body.get('result', {})

        return { 'views': r.get('views', 0), 'url': r.get('url', url), 'provider': _this() }

    def twitter(self, url=None):
        url = self._get_url(url)
        res = unirest.get('http://cdn.api.twitter.com/1/urls/count.json?url=%s' % url)

        if res.code != 200:
            return None

        return { 'shares': res.body.get('count', 0), 'url': res.body.get('url', url), 'provider': _this() }

    def tumblr(self, url=None):
        # TODO: implement
        return None

    def youtube(self, url=None):
        url = self._get_url(url)
        res = unirest.get('https://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=json' % url)

        if res.code != 200:
            return None

        r = res.body.get('entry', {})

        return { 'views': r.get('yt$statistics', {}).get('viewCount', 0),
                 'likes': r.get('yt$rating', {}).get('numLikes', 0),
                 'dislikes': r.get('yt$rating', {}).get('numDislikes', 0),
                 'url': 'https://www.youtube.com/v/%s' % url,
                 'provider': _this() }

if __name__ == '__main__':
    SC = StatsCounter('http://www.google.com')
    print('Buffer = %s' % SC.buffer())
    print('Delicious = %s' % SC.delicious())
    print('Facebook = %s' % SC.facebook())
    print('G+ = %s' % SC.google_plus())
    print('Linkedin = %s' % SC.linkedin())
    print('Pinterest = %s' % SC.pinterest())
    print('Reddit = %s' % SC.reddit('http://i.imgur.com/To3DQ6J.jpg'))
    print('StumbleUpon = %s' % SC.stumbleupon())
    print('Twitter = %s' % SC.twitter())
    print('YouTube = %s' % SC.youtube('uT3SBzmDxGk'))