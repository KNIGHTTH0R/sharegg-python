import sys

from flask import Flask, request, jsonify
from sharegg import StatsCounter

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
def get_shares(provider):
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    SC = StatsCounter(url)

    if provide == 'buffer':
        return ok(SC.buffer())
    elif provide == 'delicious':
        return ok(SC.delicious())
    elif provider in ['fb', 'facebook']:
        return ok(SC.facebook())
    elif provider in ['g+', 'google', 'googleplus']:
        return ok(SC.google_plus())
    elif provider in ['in', 'linkedin']:
        return ok(SC.linkedin())
    elif provide == 'pinterest':
        return ok(SC.pinterest())
    elif provide == 'reddit':
        return ok(SC.reddit())
    elif provide == 'stumbleupon':
        return ok(SC.stumbleupon())
    elif provider == 'twitter':
        return ok(SC.twitter())
    elif provide == 'youtube':
        return ok(SC.youtube())
    else:
        return error('Invalid provider name.')

    return error()

@app.route('/stats')
def get_stats():
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    SC = StatsCounter(url)

    stats = [SC.buffer(),
             SC.delicious(),
             SC.facebook(),
             SC.google_plus(),
             SC.linkedin(),
             SC.pinterest(),
             SC.reddit(),
             SC.stumbleupon(),
             SC.twitter(),
             SC.youtube(),]

    data = {}

    for stat in stats:
        if not stat: continue
        data[stat['provider']] = stat

    return ok(data)

def run(debug=False):
    app.debug = debug
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    run('-d' in sys.argv or '--debug' in sys.argv)