from unittest import TestCase
from pymongo import MongoClient as MC
import json
import requests
from app import app

mongo_connection = MC('localhost', 27017)
db = mongo_connection.logs
mongo_logs = db.logs

sample_log = {"origin": "postman",
              "timestamp": "now!",
              "log_level": "dev",
              "message": "this is a test of posting logs from JSON in the body!"
              }


def populate_logs(n):
    for i in range(n):
        log = sample_log
        log['item'] = str(n)
        requests.post('http://localhost:5000/?key=chunkybacon',
                      data=json.dumps(log))



class LoggingTest(TestCase):

    def setUp(self):
        pass

    def test_posting_log(self):
        response = requests.post('http://localhost:5000/?key=chunkybacon',
                                 data=json.dumps(sample_log))
        assert response.status_code is not 422
        print(response.content)
        print(type(response.content))
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
        populate_logs(100)
        response_length_3 = requests.get('http://localhost:5000/?key=chunkybacon&page=3&page_length=3')
        response_length_4 = requests.get('http://localhost:5000/?key=chunkybacon&page=3&page_length=4')
        assert len(response_length_3.content) < len(response_length_4.content)

    def tearDown(self):
        # Remove all logs
        mongo_logs.remove()
