sharegg
=======

Get social count/followers/likes/shares easily.

### Supported services

#### Shares Count

- Buffer
- Delicious
- Facebook
- Google Plus
- Linkedin
- Pinterest
- Pocket
- Reddit
- StumbleUpon
- Twitter
- VK

#### Followers Count

- G+
- Twitter

#### Others Count

- Reddit (shares, score, up, down)
- YouTube (views, favorites, likes, dislikes)

### Requirements

- Python 2.7+
- BeautifulSoup
- OAuth2
- Unirest

### Usage

#### Import

```python
from sharegg.social import Counter, Followers, Shares
```

#### Constructor

```python
C = Counter(id=None)
F = Followers(id=None)
S = Shares(id=None)
```

#### Functions

```python
# Counter
C.reddit(id=None)
C.youtube(id=None)

# Followers
F.google_plus(id=None)
F.twitter(id=None)

# Shares
S.buffer(id=None)
S.delicious(id=None)
S.facebook(id=None)
S.google_plus(id=None)
S.linkedin(id=None)
S.pinterest(id=None)
S.pocket(id=None)
S.reddit(id=None)
S.stumbleupon(id=None)
S.twitter(id=None)
S.vkontakte(id=None)
```

Function `id` param will override class `id` param.
If function and class id are a non valid value (`None`, `''`, ...), an error will be throw.

### Example

```python
from sharegg.social import Counter, Followers, Shares

import os

fb_token = os.environ.get('FB_TOKEN', '')
gplus_key = os.environ.get('GPLUS_KEY', '')
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

F = Followers(gplus_key=gplus_key, twitter_auth=twitter_auth)
print('G+ = %s' % F.google_plus('+google'))
print('Twitter = %s' % F.twitter('twitter'))

C = Counter('https://www.youtube.com/watch?v=9bZkp7q19f0')
print('Reddit = %s' % C.reddit())
print('YouTube = %s' % C.youtube())
```

and the output will be

```
Buffer = {'count': 124, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'buffer'}
Delicious = {'count': 14, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'delicious'}
Facebook = {'count': 39474777, 'id': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'facebook'}
G+ = {'count': 721806, 'id': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'google_plus'}
Linkedin = {'count': 994, 'id': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'linkedin'}
Pinterest = {'count': 19, 'id': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'pinterest'}
Pocket = {'count': 11530, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'pocket'}
Reddit = {'count': 25, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'reddit'}
StumbleUpon = {'count': 6994, 'id': u'http://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'stumbleupon'}
Twitter = {'count': 49482, 'id': u'https://www.youtube.com/watch/?v=9bZkp7q19f0', 'service': 'twitter'}
VK = {'count': 881, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'vkontakte'}

G+ = {'count': 10438727, 'id': u'https://plus.google.com/+google', 'service': 'google_plus'}
Twitter = {'count': 35259091, 'id': u'twitter', 'service': 'twitter'}

Reddit = {'service': 'reddit', 'downs': 0, 'shares': 25, 'id': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'score': 1284, 'ups': 1284}
YouTube = {'service': 'youtube', 'views': u'2242979096', 'dislikes': u'1205252', 'likes': u'9115933', 'favorites': u'0', 'id': 'https://www.youtube.com/v/9bZkp7q19f0'}
```