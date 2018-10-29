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


app = Flask(__name__)
app.config.update({
    'HAMSTER_API_BASE_URL': 'http://127.0.0.1:5000/',
    'HAMSTER_ACCESS_TOKEN_URL': 'http://127.0.0.1:5000/oauth/token',
    'HAMSTER_CLIENT_ID': 'Uddt6W5yFWLRlmc1QdV6Ajrk',
    'HAMSTER_CLIENT_SECRET': 'NDonJPvQJYiQFDV2VgsSEPWGL7q5r5Dct9SvWqGqff4JOTHu',
    'HAMSTER_CLIENT_KWARGS': {
        'grant_type': 'client_credentials',
        'scope': 'api'
    }
})


oauth = OAuth(app)
oauth.register('hamster')


@app.route('/')
def index():
    token = oauth.hamster.fetch_access_token()
    return jsonify(token)


@app.route('/curl')
def curl():
    """for example, to demonstrate running in the console."""
    template_cmd = 'curl -u {client_id}:{client_secret} -XPOST {access_token_url} -F grant_type=client_credentials -F scope=api'
    cmd = template_cmd.format(client_id=app.config['HAMSTER_CLIENT_ID'],
                              client_secret=app.config['HAMSTER_CLIENT_SECRET'],
                              access_token_url=app.config['HAMSTER_ACCESS_TOKEN_URL'])
    proc = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    token = json.loads(proc.stdout.decode())
    return jsonify(token)
