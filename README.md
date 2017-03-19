# Logging Server API Documentation

## Starting the server

The server's started as a simple Flask server; an easy way to run it is to execute with:

```bash
export FLASK_APP=logging_server.py
python3 -m flask run
```

Note that dependancies from `requirements.txt` should be installed. 

It will expect a Mongo database running locally. You can launch this on a machine with Mongo installed using the bash command `mongod`.

## Authentication

Authentication is done via an API key check. The key is supplied via a URL parameter; over SSL I don't think this would be insecure.

I know there are better ways to do this -- if I have time before needing to get this back to Amir, I'll implement something else. I haven't implemented something like that before, so I googled around and whipped up a little decorator that works, but any system where the authentication doesn't have to be done on every request would be better! Also, moving the API key from the URL parameters would really be ideal.

## Root `/`

Submitting and retrieving logs happens here! All requests to this endpoint need to be authenticated via the api key.

Examples of these can be found in the supplied unit tests.

### Submitting logs with `POST` requests
Provided the authentication system is passed, json found in the request body will be stored in the Mongo logging database.

A valid log has *at least* the keys:

* `log_level` -- the level of the log. For example, debug, error, or critical
  * Case insensitive
* `timestamp` -- the log's associated timestamp
  * This should be in ISO-8601 format
* `message` -- the actual plaintext log content
* `origin` -- the logging module, or whatever the log relates to

It can also have any other keys, however, supplied in the json in the body of the request.

### Retrieving logs with a `GET` request

Post json in the request body to filter with, suitable for filtering in PyMongo (standard mongo filtering works). If no json provided, returns everything. If any json provided, filters using that json in pymongo and returns the result. Dates will be converted to Mongo's required format, so they should be provided in ISO-8601 format in the request's json.

Retrieving logs supports pagination. To enable, add the page number as a URL parameter with the key `page`. Page length can also be parameterised; it defaults at 100, and can be changed by passing a URL parameter with the key `page_length`.

Examples of these can be found in the supplied unit tests.

---

# Logging Interface Documentation

A library is provided for logging: `logging_interface.py`. This simplifies the interaction with the server, so you don't have to clutter code with HTTP requests. 

Logging is done through the Logger class, which contains a simple log method. Typical usage might be:

```python
from logging_interface import Logger

logger = Logger(__name__, apikey=APIKEY_HERE)
logger.log("I'm a log message!")
```

Note that this will default to try to connect to a logging server on localhost at the standard Flask port (5000), with SSL enabled and no authentication to the logging server.

More detailled usage might be:

```python
from logging_interface import Logger

logger = Logger(__name__,
                apikey=APIKEY_HERE,      # A string
                server='192.168.0.123',  # A string
                port=443,                # An integer
                ssl=True)  # Or False if you swing that way

logger.log('I am a leaf on the wind',    # A string
           log_level='critical',         # A string
           extra_detail='You can add additional log details as keyword arguments here. Logs are stored on the server as Mongo documents, which are akin to a dictionary or map.',
           another_detail=12345)         # Additional log parameters can be whatever you want, so long as they're json-serialisable.
```

The logger returns a LoggingResult object informing you of the log outcome:

```python
from logging_interface import Logger

logger = Logger(__name__, apikey=APIKEY_HERE)
result = logger.log("I'm a log message!")

result.success   # A boolean indicating whether the log was sent successfully to the logging server
result.response  # A python requests library response object, to inspect if logging fails
```

## Timeouts

Note that, if the server can't be connected to at all after a timeout of 10 seconds, a ``requests.ConnectTimeout` exception will be raised.

---

# Futher implementation ideas

## Authentication

Given more time, a better authentication system would have been good to implement. Flask has a built in system that would probably work well...

## Log level hierarchy and log behaviours

It would be good to introduce some hierarchy of log levels. Python's model, with five distinct levels, would work nicely as a starting point.

Here's the thing. Python's model is particularly nice because of its *extensibility*. Each log level has an associated number (10, 20, 30...), and additional levels can be supplied to the logging module with their respective numbers, so your logs can have whatever granularity of detail.

You can also specify different behaviours of different loggers. This would take care of things like log depreciation -- easy to do with a Mongo query in another server (or building it into this logging server), but also easy if Python can take care of it for you. Log backups, redundancy, etc. can be supported with this system too -- it's really quite good.

What I'd like to do in future would be to implement something similar, with Python-like behaviour configured via a logging_levels table in Mongo, replicating the parts of the Python model we need. I'm sure other languages I'm less familiar with have similarly good examples.

## Avoiding injection attacks
I don't believe injection attacks are an issue when taking filter data from supplied parameters and feeding that directly into Mongo, because:

1. All requests for filtering are authenticated, and we should be able to trust requests which have an API key
2. Sometimes these things *do* get compromised, but even if it did, one can't insert or delete anything from Mongo via filtering

However, it should be noted that if you're taking parameters arbitrarily and filtering based on them, and there's *lots* of log data, then you might end up returning lots and lots of data! I worry that there's some sort of DDOS issue there. However, an actual real-world implementation would sanatise if this was an issue, and hopefully I'll get chance to implement better authentication anyway, which does away with some of the concerns of exporting unusually huge amounts of data via bad filtering.

---

# TODO

Things I'm still getting around to. 

* Testing the filtering mechanism (though I think this works, albeit inelegantly, for everything that isn't filtering by time or sorting)
* Implement a better response from the logging module than the LoggingResult class
