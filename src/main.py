from datetime import datetime

from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.utils import to_satoshis


def log(log_type: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = f"[{timestamp}] - [{log_type.upper()}]: {message}"
    print(msg)
    
if __name__ == "__main__":
    setup("testnet")
    # Generate a random private key
    private_key = PrivateKey()

    # Derive the public key and Bitcoin address
    public_key = private_key.get_public_key()
    address = P2pkhAddress(public_key.get_address().to_string())

    log("info",f"Private Key: {private_key.to_wif()}")
    log("info",f"Public Key: {public_key.to_hex()}")
    log("info",f"Bitcoin Address: {address.to_string()}")
    