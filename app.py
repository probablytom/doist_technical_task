from flask import Flask, request, abort
from pymongo import MongoClient as MC
from functools import wraps
import json
app = Flask(__name__)
mongo_connection = MC('localhost', 27017)
db = mongo_connection.logs
mongo_logs = db.logs


API_KEYS = ['chunkybacon']


def requires_valid_key(func):
    '''
    An authenticating decorator.
    '''
    @wraps(func)
    def auth_check(*args, **kwargs):
        key_provided = request.args.get('key')
        if key_provided in API_KEYS:
            return func(*args, **kwargs)
        else:
            abort(401)
    return auth_check


@app.route('/', methods=['POST'])
@requires_valid_key
def log_accepter():
    content = json.loads(request.data.decode())
    required_keys = ['log_level',
                     'timestamp',
                     'message',
                     'origin']

    # Check that the correct keys are supplied
    if False in [required_key in content.keys()
                 for required_key in required_keys]:
        abort(422)  # Unprocessable entity, see http://bit.ly/2nPQPCE

    # Make sure that the log level is case insensitive
    content['log_level'] = content['log_level'].upper()

    mongo_logs.insert_one(content)

    return "Posted successfully."


@app.route('/', methods=['GET'])
@requires_valid_key
def log_manager():
    print(request.args)
    return 'cheers'
