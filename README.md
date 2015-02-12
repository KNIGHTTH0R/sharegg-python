sharegg
=======

Sharegg module and Server

### Self hosting

`python sharegg/server.py`

### Server Deploy

This project is built to be deployed on [OpenShift](https://www.openshift.com/). But you can run your own self hosted server too.

### Usage

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