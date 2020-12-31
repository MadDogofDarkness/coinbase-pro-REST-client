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
    #implement method as needed for pro use
    return {"api-key":"key", "secret_key":"secret================================", "passphrase":"pass"}

class Client_Error(Exception):
    def __init__(self, message):
        self.message = message
    def __repr__(self):
        return self.message

class MarketClient():
    def __init__(self, config_file):
        self.log = []
        self.configurationfile = config_file
        if exists('log.json'):
            # self.log should be a list of log entries used to determine if data
            # requested is too old to be retrieved from cache and must be re-downloaded
            # After cache is implemented
            with open('log.json', 'r') as f:
                for line in f:
                    self.log.append(line)
        d = {}
        if type(config_file) is dict:
            d = config_file
        else:
            d = load_api_key_info(config_file)
        
        try:
            print(f"client-key: {d['client-key']}")
            self.config = d
        except KeyError:
            print("")
            return "key 'client-key' not found in loaded configuration file"
    
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
            auth = CoinbaseExchangeAuth(load_api_key_info(self.configurationfile)["api-key"], load_api_key_info(self.configurationfile)["secret_key"], load_api_key_info(self.configurationfile)["passphrase"])
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
        python analyzer.py <methodname> <endpoint> <config>
        
        the method name is the name of the method on the target api you want to call
            these can be found from the coinbase pro api documentation below:
            https://docs.pro.coinbase.com/?python#introduction
        the endpoint is the api endpoint to connect to:
            there are two endpoints, a live one and a sandbox one
            the live one will actually trade money, the sandbox lets you test first
            by default, the sandbox is the default endpoint
        
        the config is a string filename of the configuration file to be used
            if it is not passed in, a default configuration is used instead
            note: to use the config file you need to implement logic to return the file's information
            as a dictionary from the load_api_key_info() method

        """
    
    return s

def makekey():
    ck = ""
    while len(ck) < 65:
        ck += choice("0192837465ABCDEF")

    return ck

if __name__ == "__main__":
    environment = "sandbox"
    h = False
    # update config filename here or pass in command line
    configfile = {"client-key": makekey()}

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
    if len(argv) == 4:
        configfile = str(argv[3])
        with open(configfile, 'r') as f:
            d = json.load(f)
            try:
                print(d["client-key"])
            except KeyError:
                print("client-key not included in config file")
                print("automatically generating a new random key")




    client = MarketClient(configfile)
    response = client.send(method, environment)
    sleep(1)
    print(response)

    # tomorrow
    """
    implement changes to allow the user to include the filename of their desired config file on the command line,
    implement caching again



    """