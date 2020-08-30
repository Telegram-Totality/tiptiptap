import os
os.environ["TOTALITY_ENDPOINT"]="http://localhost:5000"

from decouple import config
from web3 import Web3, HTTPProvider
BOT_TOKEN=config("BOT_TOKEN")

PROVIDER = Web3(HTTPProvider(config('PROVIDER')))
DAI_CONTRACT = "0xf80A32A835F79D7787E8a8ee5721D0fEaFd78108" # Aave uses this erc20 as dai on ropsten
# Only the transfer function from the erc20 abi for simplicity reasons
DAI_ABI = [ {
    "constant": False,
    "inputs": [
      {
        "internalType": "address",
        "name": "recipient",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "transfer",
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
DAI_CONN = PROVIDER.eth.contract(address=DAI_CONTRACT, abi=DAI_ABI)