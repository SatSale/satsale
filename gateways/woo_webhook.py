import hmac
import hashlib
import json
import codecs
import time
import requests

def hook(btcpyment_secret, payload, payment):
    # Calculate a secret that is required to send back to the
    # woocommerce gateway, proving we did not modify id nor amount.
    secret_seed =  payload['amount'] * int(payload['id'])
    secret = hmac.new(btcpyment_secret, secret_seed, hashlib.sha256).hexdigest()

    # The main signature  which proves we have paid, and very recently!
    paid_time = int(time.time())
    params = {"wc-api":"wc_btcpyment_gateway", 'id' : payload['id'], 'time' : str(paid_time)}
    message = (str(paid_time) + '.' + json.dumps(params, separators=(',', ':'))).encode('utf-8')

    key = codecs.decode(secret, 'hex')
    hash = hmac.new(key, message, hashlib.sha256).hexdigest()
    headers={'Content-Type': 'application/json', 'X-Signature' : hash, 'X-Secret': secret}

    response = requests.get(
        payload['w_url'], params=params, headers=headers)

    return response
