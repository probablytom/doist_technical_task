# API Documentation

## Authentication

Authentication is done via an API key check. In the JSON provided in the request contains a `'key':apikey` pair, authentication is passed. The valid key is 'chunkybacon'.

I know there are better ways to do this -- if I have time before needing to get this back to Amir, I'll implement something else. I'm not overly familiar with this sort of tech, though, and this was the best thing I could come up with myself that seemed reasonably easy to implement off my own back. Given time, I'll implement this using Flask's built-in authentication system. 

## Root `/`

Submitting and retrieving logs happens here! All requests to this endpoint need to be authenticated via the api key.

### Submitting logs with `POST` requests
Provided the authentication system is passed, the remaining json submitted will be stored in the Mongo logging database.

### Retrieving logs with a `GET` request

Post json to filter using in Mongo. If no json provided, returns everything. If any json provided, filters using that json in pymongo and returns the result. Dates will be converted to Mongo's required format, so they should be provided in TODO format in the request's json...
