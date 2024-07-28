import os

from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.utils import to_satoshis
from blockcypher import pushtx
from dotenv import load_dotenv

from utils import log

load_dotenv()

def task2_p2sh():
    setup("testnet")
    # Create 2 private keys:
    private_key1 = PrivateKey.from_wif(os.getenv("PRIVATE_KEY"))
    private_key2 = PrivateKey.from_wif(os.getenv("PRIVATE_KEY2"))
    
    public_key1 = private_key1.get_public_key()
    public_key2 = private_key2.get_public_key()

    address1 = P2pkhAddress(public_key1.get_address().to_string())
    address2 = P2pkhAddress(public_key2.get_address().to_string())
    log("info",f"Bitcoin Address 1: {address1.to_string()}")
    log("info",f"Bitcoin Address 2: {address2.to_string()}")

    out_address = P2pkhAddress(os.getenv("OUTPUT_ADDRESS"))
     # Get UTXO and BC key
    locked_txid = os.getenv("UTXO_SH")
    locked_vout = 1
    bc_key = os.getenv("BC_API_KEY")
    
    # Creating a 2-of-2 MultiSig Scripting
    redeem_script = Script([
        'OP_2',
        public_key1.to_hex(),
        public_key2.to_hex(),
        'OP_2',
        'OP_CHECKMULTISIG'
    ])

    p2sh_address = P2shAddress.from_script(redeem_script)
    log("info",f"P2SH Address: {p2sh_address.to_string()}")
    
    tx_in = TxInput(locked_txid, locked_vout)
    tx_out= TxOutput(
        to_satoshis(0.000001),
        out_address.to_script_pub_key()
    )

    tx = Transaction([tx_in], [tx_out])
    log("info",f"\nRaw unsigned transaction:\n{tx.serialize()}")

    sig1 = private_key1.sign_input(tx,0, redeem_script)
    sig2 = private_key2.sign_input(tx,0, redeem_script)
    tx_in.script_sig = Script([
        'OP_0',
        sig1,
        sig2,
        redeem_script.to_hex()
    ])
    
    log("info",f"\nRaw signed transaction:\n{tx.serialize()}")
    
    # log("info","\nTransaction is fully signed and ready for broadcast")
    # print(pushtx(tx.serialize(), coin_symbol='btc-testnet', api_key=bc_key))
    # log("info","Transaction broadcasted successfully")
    log("info",f"\nTransaction ID: {tx.get_txid()}\n")