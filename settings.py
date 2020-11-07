from decouple import config
import os
os.environ["TOTALITY_ENDPOINT"]=config("TOTALITY_ENDPOINT")
os.environ["CUSTODIAL_ENDPOINT"]=config("CUSTODIAL_ENDPOINT")
os.environ["TOTALITY_SECRET"] = config("TOTALITY_SECRET")

TOTALITY_SECRET =  config("TOTALITY_SECRET")
from web3 import Web3, HTTPProvider
BOT_TOKEN=config("BOT_TOKEN")

USING_BOT = "CustodialTestBot"
PROVIDER = Web3(HTTPProvider(config('PROVIDER')))
DAI_CONTRACT = "0x2Aae2f090085265cd77d90b82bb8B7a908738815" # Matic Mumbai dai
# mapped to goerli 0xC1BB27a58bc4E14e49973a1345d23D6146895A9F dai


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