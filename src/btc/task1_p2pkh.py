import os

from bitcoinutils.constants import SIGHASH_ALL
from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.utils import to_satoshis
from blockcypher import pushtx
from dotenv import load_dotenv

from utils import log

load_dotenv()

def task1_p2pkh():
    setup("testnet")
    # Wallet 1:
    private_key = PrivateKey.from_wif(os.getenv("PRIVATE_KEY"))
    public_key = private_key.get_public_key()
    address = P2pkhAddress(public_key.get_address().to_string())
    log("info",f"Bitcoin Address: {address.to_string()}")
    out_address = P2pkhAddress(os.getenv("OUTPUT_ADDRESS"))
    
    # Get UTXO and BC key
    locked_txid = os.getenv("UTXO_KH")
    locked_vout = 1
    bc_key = os.getenv("BC_API_KEY")

    # UTXO Balance, Amount2Spent, Fee and Change Amount
    # Go https://live.blockcypher.com/btc-testnet/tx/{transaction_id} // Search
    # with the UTXO_KH in .env
    # and get by hand the balance of the output have amount larger than 0.000001
    balance = to_satoshis(0.000087)
    amount2send = to_satoshis(0.000001)
    fee = to_satoshis(0.000001)
    change = balance - amount2send - fee

    #P2PKH transaction example with 1 input and 2 outputs( 1 receiver and 1 myself)
    tx_in = TxInput(locked_txid, locked_vout)
    tx_out = TxOutput(
        amount2send,
        Script([
            'OP_DUP',
            'OP_HASH160',
            out_address.to_hash160(),
            'OP_EQUALVERIFY',
            'OP_CHECKSIG'
        ])
    )
    change_txout = TxOutput(
        change,
        Script([
            'OP_DUP',
            'OP_HASH160',
            address.to_hash160(),
            'OP_EQUALVERIFY',
            'OP_CHECKSIG'
        ])
    )
    # Lock Funds        
    tx = Transaction([tx_in], [tx_out, change_txout], has_segwit=True)
    log("info",f"\nRaw unsigned transaction:\n{tx.serialize()}")
    # Sign the transaction to spend the locked funds
    sig = private_key.sign_input(tx, 0, Script(['OP_DUP', 'OP_HASH160', address.to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG']))
    tx_in.script_sig = Script([sig, public_key.to_hex()])
    log("info",f"\nRaw signed transaction:\n{tx.serialize()}")
    print(pushtx(tx.serialize(), coin_symbol='btc-testnet', api_key=bc_key))

    log("info",f"\nTransaction ID: {tx.get_txid()}\n")