from decouple import config
import os
os.environ["TOTALITY_ENDPOINT"]=config("TOTALITY_ENDPOINT")
#os.environ["TOTALITY_SECRET"] = "6666"

from web3 import Web3, HTTPProvider
BOT_TOKEN=config("BOT_TOKEN")
TOTALITY = config("TOTALITY_ENDPOINT")
PROVIDER = Web3(HTTPProvider(config('PROVIDER')))


