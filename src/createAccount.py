from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.utils import to_satoshis

if __name__ == "__main__":
    # Generate a random private key
    private_key = PrivateKey()

    # Derive the public key and Bitcoin address
    public_key = private_key.get_public_key()
    address = P2pkhAddress(public_key.get_address().to_string())

    print("Private Key: ", private_key.to_wif())
    print("Public Key: ", public_key.to_hex())
    print("Bitcoin Address: ", address.to_string())