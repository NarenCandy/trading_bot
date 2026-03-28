import hashlib
import hmac
import time
import urllib.parse
import httpx
from bot.logging_config import get_logger
logger = get_logger(__name__)

#load_dotenv() # moved to cli.py so to avoid duplicat as this is already loaded in cli.py 

BASE_URL = "https://testnet.binancefuture.com"

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = httpx.Client(
            base_url=BASE_URL,
            headers={"X-MBX-APIKEY": self.api_key}
        )

    def _sign(self, params):
        query_string = urllib.parse.urlencode(params)
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _signed_request(self, method, path, params):   
        params["timestamp"] = int(time.time() * 1000)
        params["signature"] = self._sign(params)
        logger.info(f"Sending {method} to {path} | params: {list(params.keys())}")

        if method == "GET":
            resp = self.client.get(path, params=params)
        else:
            resp = self.client.post(path, data=params)

        if resp.status_code != 200:
            logger.error(f"Binance error {resp.status_code}: {resp.text}")

        resp.raise_for_status()
        logger.info(f"Response {resp.status_code}: {resp.text[:200]}")

        return resp.json()

    def place_order(self, **kwargs):                   
        return self._signed_request("POST", "/fapi/v1/order", kwargs)