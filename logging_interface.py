import requests
import json
from requests import Response
from datetime import datetime


class LoggingResult:
    '''
    A logging result class. Works out whether the log has been successful, and
    if not, contains the response from the logging request.

    Note: I've designed this this way because there's a myriad of things that
    *can* go wrong. Rather than trying to address as many as possible when writing
    this in a deadline, I've designed it to get out of the way of diagnosing the
    cause of the problem.

    I know this isn't good design. It means that actual code using this library
    would get littered with code dealing with all of the possible issues that can
    arise from the logging, instead of the library handling it and returning useful
    errors when it can't resolve the issue itself!

    In future, if I was spending more
    time on this project, I'd get rid of this class and instead return an integer
    success code. The success code would be the code returned by the server, and
    before returning errors (non-200 codes), it would see whether it could resolve
    any of those issues itself.

    My suspicion is that, in practice, any actual errors which would arise would
    come from either something like the recent AWS outage in which case, cache
    the log messages in memory and retry periodically), or bad configuration
    on the part of the programmer (which we can't help anyway).
    '''
    def __init__(self,
                 success: bool,
                 response: Response):
        self.response = response
        self.success = success


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
        self.server = server
        self.port = port
        self.apikey = apikey
        self.protocol = 'http'
        if ssl:
            self.protocol += 's'

    def log(self,
            message: str,
            log_level: str = 'debug',
            **kwargs):
        '''
        Submit a log message.
        Log levels are optional, and default to `debug`.
        '''

        # Construct the base url in the log method, not the init method, so that
        # if the api key/server/etc is changed due to a previous error, updated
        # connection details are acknowledged.
        base_url = self.protocol + '://' + self.server + ':' + str(self.port) + '/'

        if self.apikey is not None:
            base_url += '?key='+self.apikey

        timestamp = datetime.now().isoformat()
        log = {'message': message,
               'timestamp': timestamp,
               'log_level': log_level,
               'origin': self.origin}

        # Don't let supplementary details override the log details
        [kwargs.pop(key, None) for key in log.keys()]

        # Extend the log with the supplementary details
        for key, value in kwargs.items():
            log[key] = value

        response = requests.post(base_url, data=json.dumps(log))

        return LoggingResult(response.status_code == 200, response)
