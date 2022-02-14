# A contract that 
# 1. deploys to a local Ganache Instance
# 2. checks the value of a variable
# 3. updates that value through another transaction
# 4. and then checks again


from web3 import Web3
import json
import os
from dotenv import load_dotenv
# Using a compiler because solidity is a compiled language
from solcx import compile_standard, install_solc

load_dotenv()

# So we open a file, read it into a variable, and then close it
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

print("Installing...")
install_solc("0.6.0")

# we're compiling our solidity file here and then dumping the executable in to a JSON file (so the ABI and bytecode etc. of our contract will be there)
# There's a lot of low level implementation here, the details don't super matter. If you want to know more, go to the documentation for solcx etc.
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources":{"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
           "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# dumps the compiled solidity to a JSON file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode from JSON
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi from JSON
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

# We  are deploying to the Rinkeby test net using our MetaMask
w3 = Web3(Web3.HTTPProvider(os.getenv("RINKEBY_RPC_URL"))) # stored in env variables (we got this address from infura.io)
chain_id = 4 # we got this chain ID from chainlist.org
my_address = "0x19BB59cee18d38e1DeD6B4816d424B084cE0008A" # my personal rinkeby testnet address
private_key = os.getenv("PRIVATE_KEY") # also stored in env variables, my personal private key for the test net account


# If we were connecting to a local Ganache block chain - we get this info from the Ganache CLI output/the Ganache UI
# w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# chain_id = 1337
# my_address = "0x484A0e84C2432792Bf0b374DE612918F1548E368"
# private_key = os.getenv("PRIVATE_KEY")



# Create the contract object
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# Submit the transaction that deploys the contract
# the constructor here is empty, because we aren't initializing any state variables for this contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
print("Deploying Contract!")
# Send transaction to the blockchain
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# Wait for the transaction to be mined, and get the transaction receipt after it's mined into the chain 
print("Waiting for transaction to finish...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Done! Contract deployed to {tx_receipt.contractAddress}")


# So now the contract is deployed to the chain
# And now below we can interact with the contract on-chain


# Working with deployed Contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# We have to use the .call() method to actually call the retrieve function
# There are two ways we can call functions on contracts, either with .call() or with .transact()
# If we do .transact() then we are actually making a state change to the chain, which will require gas
print(f"Initial Stored Value {simple_storage.functions.retrieve().call()}")

# below we are making a state change on the blockchain and updating the favorite number to 15
# Opposed to just calling the function, which wouldn't actually make a state change to the chain etc.
greeting_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_greeting_txn = w3.eth.account.sign_transaction(
    greeting_transaction, private_key=private_key
)
tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
print("Updating stored Value...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)

print(simple_storage.functions.retrieve().call())