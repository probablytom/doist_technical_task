from unittest import TestCase
from pymongo import MongoClient as MC
import json
import requests
from app import DEFAULT_PAGE_LENGTH
from logging_interface import Logger
from copy import copy
from datetime import datetime

mongo_connection = MC('localhost', 27017)
db = mongo_connection.logs
mongo_logs = db.logs

logger = Logger('unittests', ssl=False, apikey='chunkybacon')

sample_log = {"origin": "unittest_sample_log",
              "timestamp": datetime.now().isoformat(),
              "log_level": "dev",
              "message": "this is a test of posting logs from JSON in the body!"
              }


def populate_logs(n):
    for i in range(n):
        log = sample_log
        log['item'] = str(n)
        requests.post('http://localhost:5000/?key=chunkybacon',
                      data=json.dumps(log))


class LoggingServerTest(TestCase):

    def test_posting_log(self):
        response = requests.post('http://localhost:5000/?key=chunkybacon',
                                 data=json.dumps(sample_log))
        assert response.status_code is not 422
        assert response.content == b'Posted successfully.'

    def test_authentication(self):
        response_auth = requests.post('http://localhost:5000/?key=chunkybacon',
                                      data=json.dumps(sample_log))
        response_no_auth = requests.post('http://localhost:5000/',
                                         data=json.dumps(sample_log))
        assert response_no_auth.status_code == 401
        assert response_auth.status_code is not 422
        assert response_auth.content == b'Posted successfully.'

    def test_pagination_page_parameter(self):
        populate_logs(100)
        response = requests.get('http://localhost:5000/?key=chunkybacon&page=1')
        assert response.content.decode() != b'[]'

    def test_pagination_limit_length(self):
        populate_logs(200)
        response_no_limit = requests.get('http://localhost:5000/?key=chunkybacon&page=1')
        response_length_3 = requests.get('http://localhost:5000/?key=chunkybacon&page=1&page_length=3')
        response_length_4 = requests.get('http://localhost:5000/?key=chunkybacon&page=1&page_length=4')
        assert len(response_length_3.content) < len(response_length_4.content)
        assert len(json.loads(response_no_limit.content.decode())) == DEFAULT_PAGE_LENGTH

    def test_incomplete_log(self):
        log = copy(sample_log)
        log.pop('log_level')
        response = requests.post('http://localhost:5000/?key=chunkybacon',
                                 data=json.dumps(log))
        assert response.status_code == 422

    def tearDown(self):
        # Remove all logs from the tests after they run
        mongo_logs.remove()


class LoggingCLientLibraryTest(TestCase):

    def test_posting_log(self):
        response = logger.log('this is a test')
        assert response.success
