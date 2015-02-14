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
def root():
    return 'Sharegg server is running.'

@app.route('/stats/<service>')
@crossdomain(origin='*')
def get_shares(service):
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    C = Counter(url)

    try:
        if service == 'buffer':
            return ok(C.buffer())
        elif service == 'delicious':
            return ok(C.delicious())
        elif service in ['fb', 'facebook']:
            return ok(C.facebook())
        elif service in ['g+', 'google', 'googleplus']:
            return ok(C.google_plus())
        elif service in ['in', 'linkedin']:
            return ok(C.linkedin())
        elif service == 'pinterest':
            return ok(C.pinterest())
        elif service == 'pocket':
            return ok(C.pocket())
        elif service == 'reddit':
            return ok(C.reddit())
        elif service == 'stumbleupon':
            return ok(C.stumbleupon())
        elif service == 'twitter':
            return ok(C.twitter())
        elif service == 'youtube':
            return ok(C.youtube())
        elif service in ['vk', 'vkontakte']:
            return ok(C.vkontakte())
        else:
            return error('Invalid service name.')
    except:
        return error('Can\'t retrieve information data.')

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
        data[stat['service']] = stat

    return ok(data)

def run(host='0.0.0.0', port=8080, debug=False):
    app.debug = debug
    app.jinja_env.cache = {}
    app.run(host=host, port=port)

if __name__ == "__main__":
    run(debug='-d' in sys.argv or '--debug' in sys.argv)