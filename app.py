from flask import Flask, request, abort
from pymongo import MongoClient as MC
from functools import wraps
app = Flask(__name__)
mongo_connection = MC('localhost', 27017)
mongo_logs = mongo_connection.logs

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
    raise NotImplemented('Yet to write this!')


@app.route('/', methods=['GET'])
@requires_valid_key
def log_manager():
    raise NotImplemented('Yet to write this!')
