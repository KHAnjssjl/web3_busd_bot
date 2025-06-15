from web3 import Web3
import time

bsc_rpc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_rpc))

sender_address = "0x9f4B4a826ecfD42a25c123c5e1a44D0f565Ea25F"
sender_private_key = "096d7d5fb530ee919f982ead2a169940354ebfeb54f15d0de646ba389da65d42"
receiver_address = "0x14A44E33942e7654746835dbF0Ee52871CD647b9"

busd_contract_address = web3.to_checksum_address("0xe9e7cea3dedca5984780bafc599bd69add087d56")
busd_abi = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
]

busd = web3.eth.contract(address=busd_contract_address, abi=busd_abi)

def send_busd():
    balance = busd.functions.balanceOf(sender_address).call()
    if balance > 0:
        nonce = web3.eth.get_transaction_count(sender_address)
        tx = busd.functions.transfer(receiver_address, balance).build_transaction({
            'chainId': 56,
            'gas': 80000,
            'gasPrice': web3.to_wei('0.1', 'gwei'),
            'nonce': nonce
        })
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=sender_private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print("BUSD sent. Tx hash:", web3.toHex(tx_hash))
    else:
        print("No BUSD to transfer.")

while True:
    try:
        send_busd()
        time.sleep(0.1)
    except Exception as e:
        print("Error:", e)
        time.sleep(0.1)

