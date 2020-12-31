import json
# test ♥
import requests
from requests.exceptions import ConnectionError
from time import time, sleep
from Auth import CoinbaseExchangeAuth
from random import choice
from sys import argv
from os.path import exists

def check_filename(filename, logs):
    t = int(time())
    for l in logs:
        if l[0] == filename:
            if l[1] > t + 5:
                print("filename found in logs")
                return True
    
    print("filename not found in logs")
    return False

def load_api_key_info(file_to_load_from):
    return {"api-key":"key", "secret_key":"secret================================", "passphrase":"pass"}

class Client_Error(Exception):
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return self.message

class MarketClient():
    def __init__(self, config_file):
        self.log = []
        if exists('log.json'):
            # self.log should be a list of log entries used to determine if data requested is too old to be retrieved from cache and must be re-downloaded
            with open('log.json', 'r') as f:
                for line in f:
                    self.log.append(line)
        d = {}
        if type(config_file) is dict:
            d = config_file
        else:
            with open(config_file, 'r') as f:
                try:
                    d = json.load(f)
                except FileNotFoundError:
                    print("Error: config file could not be either found, loaded or read.")
        
        try:
            print(f"client-key: {d['client-key']}")
            self.config = d
        except KeyError:
            return "key 'api-key' not found in loaded configuration file"
    
    def save(self):
        return False

    
    def send(self, method, endpoint):
        url_base = ""
        filename = (method + "-" + endpoint + ".json").replace('/', '#')

        if endpoint == "live":
            url_base = "https://api.pro.coinbase.com/"
        elif endpoint == "sandbox":
            url_base = "https://api-public.sandbox.pro.coinbase.com/"
        else:
            return Client_Error("Client Error: endpoint not specified, must be either 'live' or 'sandbox' to work.")

        if url_base == "":
            print("An error occurred when processing the client endpoint connection")
            return Client_Error("An error occurred when processing the client endpoint connection")
        else:
            url = url_base + method
            auth = CoinbaseExchangeAuth(load_api_key_info("keys.txt")["api-key"], load_api_key_info("keys.txt")["secret_key"], load_api_key_info("keys.txt")["passphrase"])
            response = False
            
            try:
                response = requests.get(url=url, auth=auth)
                #print(f"status code debug: {response.status_code}")
            except ConnectionError:
                print(f"the server at {url} is not responding")
                return False

            if response:
                print(f"Response status code: {response.status_code}")
                d = json.loads(response.content)
                return json.dumps(d, indent=4, ensure_ascii=True)
            else:
                print(f"Response was not recieved from the server at {url}")
                return False


def help():
    """
    the help method
    """
    s = """
        usage:
        python analyzer.py <methodname> <endpoint>
        
        the method name is the name of the method on the target api you want to call
        these can be found from the coinbase pro api documentation

        the endpoint is the api endpoint to connect to:
            there are two endpoints, a live one and a sandbox one
            the live one will actually trade money, the sandbox lets you test first
            https://stackoverflow.com/questions/6346492/how-to-stop-a-for-loop
        """
    
    return s


if __name__ == "__main__":
    environment = "sandbox"
    h = False
    if len(argv) < 2:
        h = True

    for arg in argv:
        if arg in ["-h", "help", "--h", "--help", "man", "-help"]:
            h = True
    
    if h:
        print(help())
        exit()

    if len(argv) >= 2:
        method = str(argv[1])
    if len(argv) == 3:
        environment = str(argv[2])

    ck = ""
    while len(ck) < 65:
        ck += choice("0192837465ABCDEF")

    client = MarketClient({"client-key":ck})
    response = client.send(method, environment)
    sleep(1)
    print(response)