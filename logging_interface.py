import requests
import json
from datetime import datetime


class Logger:
    '''
    The Client-side library to the Doist technical task logging server.
    General usage: logger = Logger(__name__, apikey=APIKEY_HERE).
    Parameters let you set:
        server: the domain/ip the logging server is running on (string)
        port:   the port to log to (int)
        apikey: the apikey to use for authentication (string)
        ssl:    whether to use SSL (boolean)
    '''
    def __init__(self,
                 origin: str,
                 server: str = 'localhost',
                 port:   int = 5000,
                 apikey: str = None,
                 ssl:    bool = True):
        self.origin = origin
        self.apikey = apikey
        protocol = 'http'
        if ssl:
            protocol += 's'
        self.base_url = protocol + '://' + server + ':' + port + '/'

        if self.apikey is not None:
            self.base_url += '?key='+self.apikey

    def log(self,
            message: str,
            log_level: str = 'debug',
            **kwargs):
        '''
        Submit a log message.
        Log levels are optional, and default to `debug`.
        '''
        timestamp = datetime.now().isoformat()
        log = {'message': message,
               'timestamp': timestamp,
               'log_level': log_level,
               'origin': self.origin}

        # Don't let supplementary details override the log details
        [kwargs.pop(key) for key in log.keys()]

        # Extend the log with the supplementary details
        for key, value in kwargs.items():
            log[key] = value

        response = requests.post(self.baseurl, data=json.dumps(log))
