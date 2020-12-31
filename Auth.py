import json, hmac, hashlib, time, requests, base64, datetime
from requests.auth import AuthBase

# Create custom authentication for Exchange
class CoinbaseExchangeAuth(AuthBase):
    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = base64.b64encode(hashlib.sha1(str.encode(secret_key, 'utf-8')).digest())
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(datetime.datetime.utcnow()) + " UTC"
        message = str.encode(timestamp + request.method + request.path_url + (request.body or ''), 'utf-8')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        #print(signature.digest())
        signature_b64 = base64.b64encode(signature.digest())
        #print(signature_b64)

        d = {
        "CB-ACCESS-KEY" : self.api_key,
        "CB-ACCESS-TIMESTAMP" : timestamp,
        "CB-ACCESS-SIGN": signature_b64.decode('utf-8'),
        "CB-ACCESS-PASSPHRASE": self.passphrase,
        "Content-Type": "application/json",
        "Server": "CherryPiv0.1.2",
        "X-Forwarded-For": "127.0.0.1",
        "X-Frame-Options": "deny",
        "X-Powered-By": "Python - client design by AtiCawl LLC"
        }
        #print(json.dumps(d, indent=4, ensure_ascii=True))# debug
        request.headers.update(d)

        return request


if __name__ == "__main__":
    print("auth module loaded")
    print("haskell implementation of http3 https://github.com/kazu-yamamoto/http3/tree/master/Network/HTTP3")
