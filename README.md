sharegg
=======

Get social count/shares/likes easily.

### Supported services

- Buffer
- Delicious
- Facebook
- Google Plus
- Linkedin
- Pinterest
- Reddit
- StumbleUpon
- Twitter
- VK
- YouTube

### Usage

#### Import

```python
from sharegg.social import Counter
```

#### Contructor

```python
C = Counter(url=None)
```

#### Functions

```python
C.buffer(url=None)
C.delicious(url=None)
C.facebook(url=None)
C.google_plus(url=None)
C.linkedin(url=None)
C.pinterest(url=None)
C.reddit(url=None)
C.stumbleupon(url=None)
C.twitter(url=None)
C.vkontakte(url=None)
C.youtube(url=None)
```

Function `url` param will override class `url` param.
If function and class url are a non valid value (`None`, `''`, ...), an error will be throw.

### Example

```python
from sharegg.social import Counter

C = Counter('https://www.youtube.com/watch?v=9bZkp7q19f0')

print('Buffer = %s' % C.buffer())
print('Delicious = %s' % C.delicious())
print('Facebook = %s' % C.facebook())
print('G+ = %s' % C.google_plus())
print('Linkedin = %s' % C.linkedin())
print('Pinterest = %s' % C.pinterest())
print('Reddit = %s' % C.reddit())
print('StumbleUpon = %s' % C.stumbleupon())
print('Twitter = %s' % C.twitter())
print('VK = %s' % C.vkontakte())
print('YouTube = %s' % C.youtube())
```

and the output will be

```
Buffer = {'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'buffer', 'shares': 124}
Delicious = {'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'delicious', 'shares': 14}
Facebook = {'url': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'facebook', 'likes': 13292077, 'shares': 12732543}
G+ = {'url': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'g+', 'shares': 719441.0}
Linkedin = {'url': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'linkedin', 'shares': 994}
Pinterest = {'url': u'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'pinterest', 'shares': 18}
Reddit = {'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'downs': 0, 'score': 1281, 'ups': 1281, 'service': 'reddit'}
StumbleUpon = {'url': u'http://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'stumbleupon', 'views': 6994}
Twitter = {'url': u'https://www.youtube.com/watch/?v=9bZkp7q19f0', 'service': 'twitter', 'shares': 49312}
VK = {'count': '880', 'url': 'https://www.youtube.com/watch?v=9bZkp7q19f0', 'service': 'vkontakte'}
YouTube = {'url': 'https://www.youtube.com/v/9bZkp7q19f0', 'dislikes': u'1203592', 'likes': u'9108139', 'service': 'youtube', 'views': u'2240589305'}
```

### Self hosting

`python sharegg/server.py` or `python -m sharegg.server`

### Server Deploy

This project is built to be deployed on [OpenShift](https://www.openshift.com/). But you can run your own self hosted server too.