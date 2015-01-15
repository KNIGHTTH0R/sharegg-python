import sys

from cors import crossdomain
from flask import Flask, request, jsonify
from social import Counter

app = Flask(__name__)

def status(body, code):
    res = jsonify(body)
    res.status_code = code
    return res

def ok(data):
    return status(data, 200)

def error(msg='Unknown error.', code=400):
    return status({ 'message' : msg }, code)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/stats/<provider>')
@crossdomain(origin='*')
def get_shares(provider):
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    C = Counter(url)

    if provider == 'buffer':
        return ok(C.buffer())
    elif provider == 'delicious':
        return ok(C.delicious())
    elif provider in ['fb', 'facebook']:
        return ok(C.facebook())
    elif provider in ['g+', 'google', 'googleplus']:
        return ok(C.google_plus())
    elif provider in ['in', 'linkedin']:
        return ok(C.linkedin())
    elif provider == 'pinterest':
        return ok(C.pinterest())
    elif provider == 'reddit':
        return ok(C.reddit())
    elif provider == 'stumbleupon':
        return ok(C.stumbleupon())
    elif provider == 'twitter':
        return ok(C.twitter())
    elif provider == 'youtube':
        return ok(C.youtube())
    elif provider in ['vk', 'vkontakte']:
        return ok(C.vkontakte())
    else:
        return error('Invalid provider name.')

    return error()

@app.route('/stats')
@crossdomain(origin='*')
def get_stats():
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    C = Counter(url)

    stats = [C.buffer(),
             C.delicious(),
             C.facebook(),
             C.google_plus(),
             C.linkedin(),
             C.pinterest(),
             C.reddit(),
             C.stumbleupon(),
             C.twitter(),
             C.youtube(),
             C.vkontakte(),]

    data = {}

    for stat in stats:
        if not stat: continue
        data[stat['provider']] = stat

    return ok(data)

def run(host='0.0.0.0', port=8080, debug=False):
    app.debug = debug
    app.jinja_env.cache = {}
    app.run(host=host, port=port)

if __name__ == "__main__":
    run(debug='-d' in sys.argv or '--debug' in sys.argv)