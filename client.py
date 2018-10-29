# coding: utf-8
#
# Copyright 2018 Kirill Vercetti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import subprocess

from flask import Flask, jsonify
from authlib.flask.client import OAuth


def fetch_token():
    with open('token.json') as f:
        return json.load(f)


def save_token(token):
    with open('token.json', 'w') as f:
        json.dump(token, f, indent=4)


app = Flask(__name__)
app.config.update({
    'HAMSTER_API_BASE_URL': 'http://127.0.0.1:5000/api/',
    'HAMSTER_ACCESS_TOKEN_URL': 'http://127.0.0.1:5000/oauth/token',
    'HAMSTER_CLIENT_ID': 'COOoo86pX3xCwao5RxwBFZ09',
    'HAMSTER_CLIENT_SECRET': 'P9wUsjYkF7hHnJK5D0WBjU9c6yibdYX3oktQ1reDG0c2VlIY',
    'HAMSTER_CLIENT_KWARGS': {
        'grant_type': 'client_credentials',
        'scope': 'profile'
    }
})


oauth = OAuth(app)
oauth.register('hamster', fetch_token=fetch_token)


@app.route('/')
def index():
    resp = oauth.hamster.get('me')
    return jsonify(resp.json())


@app.route('/authorize')
def authorize():
    token = oauth.hamster.fetch_access_token()

    if token:
        save_token(token)

    return jsonify(token)


@app.route('/curl')
def curl():
    """for example, to demonstrate running in the console."""
    template_cmd = 'curl -u {client_id}:{client_secret} -XPOST {access_token_url} -F grant_type=client_credentials -F scope=profile'
    cmd = template_cmd.format(client_id=app.config['HAMSTER_CLIENT_ID'],
                              client_secret=app.config['HAMSTER_CLIENT_SECRET'],
                              access_token_url=app.config['HAMSTER_ACCESS_TOKEN_URL'])

    proc = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    token = json.loads(proc.stdout.decode())

    if token:
        save_token(token)

    return jsonify(token)
