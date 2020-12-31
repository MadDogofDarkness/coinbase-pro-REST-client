# coinbase-pro-REST-client
A client in python for the coinbase pro REST api.
After I figure out how to install required modules, I'll update the client to do that as long as permissions are granted.

Designed on Python 3.7.4
Should be compatible with everything above that, and most likely down to whenever they added in f strings.
Not tested on python 2.x.x

Requirements:
All modules require json and requests

clientmodule:
time, Auth, random, sys, os.path

Auth:
hmac, hashlib, time, requests, base64, datetime

The Auth module, handles authentication and is copied from the coinbase pro api website, with a few modifications to make it work.
https://docs.pro.coinbase.com/?python#authentication

The client module handles making the request to their api and responding with either the correct output or an informative error.
By default, the client will enforce a second delay before returning the response, in order to ensure that too many requests are not made to the api.
This is just a call to sleep(1) and can be easily removed if desired without impacting functionality.

The fields needed in the config file are:
api-key, secret_key, and passphrase

By default, all requests will go to the sandbox endpoint for their api.
To make requests to the production API,you will need to create your own api key, and save the necessary credentials for retrieval.
There is a method to load these credentials, which is integrated into the class already. You will need to fill in this method with whatever method is needed to retrieve your
credentials from wherever they are generated or stored. This is the load_api_key_info() method.
After updating the method with the necessary logic, you would need to update the MarketClient instance
client = MarketClient({"client-key":ck})
with the filename of your configuration file or a dictionary containing the credentials with the necessary keys.

