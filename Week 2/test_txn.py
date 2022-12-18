from algosdk.v2client import algod
from algosdk.future import transaction
from algosdk import account, mnemonic, constants
import json
import base64

def generate_algorand_keypair():
    private_key, address = account.generate_account()
    print("My address: {}".format(address))
    print("My private key: {}".format(private_key))
    print("My passphrase: {}".format(mnemonic.from_private_key(private_key)))

passphrase = "oak south indoor offer cross course idle jeans mail jump attitude width public enemy that various hill sudden bargain stove away inject lion abandon reject"
address = "67UKE7KGUAMK4GKJL3FQ2XDMVYATMOZQSHZAZ2QIKL7Y57Q334COUVOHUM"

# generate_algorand_keypair()

def first_transaction_example(my_mnemonic, my_address):
    algo_address = "https://testnet-api.algonode.cloud"
    algo_client = algod.AlgodClient("", algo_address)

    print("My address: {}".format(my_address))
    private_key = mnemonic.to_private_key(my_mnemonic)
    account_info = algo_client.account_info(my_address)
    print("Account balance: {} microAlgos".format(account_info.get("amount")))

    #build transaction
    params = algo_client.suggested_params()
    print(params.fee)

    params.flat_fee = constants.MIN_TXN_FEE
    params.fee = 1000
    receiver = "HZ57J3K46JIJXILONBBZOHX6BKPXEM2VVXNRFSUED6DKFD5ZD24PMJ3MVA"
    amount = 1000
    note = "Hello".encode()

    unsigned_txn = transaction.PaymentTxn(my_address, params, receiver, amount, None, note)

    #signed transaction
    signed_txn = unsigned_txn.sign(private_key)

    #submit transaction
    txid = algo_client.send_transaction(signed_txn)
    print("Signed transaction with txId: {}".format(txid))

    #wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algo_client, txid, 4)
    except Exception as err:
        print(err)
        return

    print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
    print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))

    print("Starting Account Balance: {} microAlgos".format(account_info.get("amount")))
    print("Amount transferred: {} micorAlgos".format(amount))
    print("Fee: {} microAlgos".format(params.fee))


first_transaction_example(passphrase, address)
    