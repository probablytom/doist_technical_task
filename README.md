# API Documentation

## Authentication

Authentication is done via an API key check. In the JSON provided in the request contains a `'key':apikey` pair, authentication is passed. The valid key is 'chunkybacon'.

I know there are better ways to do this -- if I have time before needing to get this back to Amir, I'll implement something else. I'm not overly familiar with this sort of tech, though, and this was the best thing I could come up with myself that seemed reasonably easy to implement off my own back. Given time, I'll implement this using Flask's built-in authentication system. 

## Root `/`

Submitting and retrieving logs happens here! All requests to this endpoint need to be authenticated via the api key.

### Submitting logs with `POST` requests
Provided the authentication system is passed, the remaining json submitted will be stored in the Mongo logging database.

A valid log has *at least* the keys:

* `log_level` -- the level of the log. For example, debug, error, or critical.
  * Case insensitive.
* `timestamp` -- the log's associated timestamp
  * This should be in TODOTODOTODO format
* `message` -- the actual plaintext log content
* `origin` -- the logging module, or whatever the log relates to

### Retrieving logs with a `GET` request

Post json to filter using in Mongo. If no json provided, returns everything. If any json provided, filters using that json in pymongo and returns the result. Dates will be converted to Mongo's required format, so they should be provided in TODO format in the request's json...

---

# Futher implementation ideas

## Authentication

Given more time, a better authentication system would have been good to implement. Flask has a built in system that would probably work well...

## Log level hierarchy

It would be good to introduce some hierarchy of log levels...Python's model, with five distinct levels, would work nicely.

Here's the thing. Python's model is particularly nice because of its *extensibility*. Each log level has an associated number (10, 20, 30...), and additional levels can be supplied to the logging module with their respective numbers.

What I'd like to do in future would be to implement something similar, with Python-like behaviour configured via a logging_levels table in Mongo.

### Log behaviours

Similarly, logging behaviour could be configured via Mongo, for the depreciation notes etc in the Gist spec. However, that's quite beyond me for a 10 hour task! A lot of the default Python logging behaviour sounds useful for the original gist, but just handing over to Python's native logger isn't very interesting as a solultion to this challenge, so while I've been told to keep it simple, I've avoided Python's internal logging mechanisms intentionally.
