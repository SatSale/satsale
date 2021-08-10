import socks
import json
import requests
import time

import config

time.sleep(3)

print("Using tor proxies {}".format(config.tor_proxy))
session = requests.session()
session.proxies = {
    "http": "socks5h://{}".format(config.tor_proxy),
    "https": "socks5h://{}".format(config.tor_proxy)
}

print(
    "Checking tor circuit IP address... You should check this is different to your IP."
)
r = session.get("http://httpbin.org/ip")
print(r.text)
