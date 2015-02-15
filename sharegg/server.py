import sys

from cors import crossdomain
from flask import Flask, request, jsonify
from social import Shares

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

@app.route('/social/shares/<service>')
@crossdomain(origin='*')
def get_shares(service):
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    S = Shares(url, app.fb_token)

    try:
        if service == 'buffer':
            return ok(S.buffer())
        elif service == 'delicious':
            return ok(S.delicious())
        elif service in ['fb', 'facebook']:
            return ok(S.facebook())
        elif service in ['g+', 'google', 'googleplus']:
            return ok(S.google_plus())
        elif service in ['in', 'linkedin']:
            return ok(S.linkedin())
        elif service == 'pinterest':
            return ok(S.pinterest())
        elif service == 'pocket':
            return ok(S.pocket())
        elif service == 'reddit':
            return ok(S.reddit())
        elif service == 'stumbleupon':
            return ok(S.stumbleupon())
        elif service == 'twitter':
            return ok(S.twitter())
        elif service == 'youtube':
            return ok(S.youtube())
        elif service in ['vk', 'vkontakte']:
            return ok(S.vkontakte())
        else:
            return error('Invalid service name.')
    except:
        return error('Can\'t retrieve information data.')

@app.route('/social/shares')
@crossdomain(origin='*')
def get_all_shares():
    url = request.args.get('url')

    if not url:
        return error('Parameter "url" is required.')

    S = Shares(url, app.fb_token)

    try:
        shares = [S.buffer(),
                  S.delicious(),
                  S.facebook(),
                  S.google_plus(),
                  S.linkedin(),
                  S.pocket(),
                  S.pinterest(),
                  S.reddit(),
                  S.stumbleupon(),
                  S.twitter(),
                  S.vkontakte(),]
    except:
        return error('Can\'t retrieve information data.')

    data = {}

    for share in shares:
        if not share: continue
        data[share['service']] = share

    return ok(data)

def run(host='0.0.0.0', port=8080, debug=False, fb_token=None):
    app.debug = debug
    app.jinja_env.cache = {}
    app.fb_token = fb_token
    app.run(host=host, port=port)

if __name__ == "__main__":
    import os
    run(fb_token=os.environ.get('FB_TOKEN', ''),debug='-d' in sys.argv or '--debug' in sys.argv)