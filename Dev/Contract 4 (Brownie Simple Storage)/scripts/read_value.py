from brownie import SimpleStorage, accounts, config

# The SimpleStorage array is basically an array of all the contracts that we've deployed in this brownie project. It knows all the contracts because every time we deploy a new one in this project it will store it in the build/deployments directory
# Every time we deploy a new contract, we deploy a new smart contract to a unique address
# Every time we make a state change to an existing contract, we send a transaction with the details of that change to the address of the contract in question
# So if you query for all transactions of the smart contract, you'll be able to see its creation but also all the state changes, and so the software is able to easily pull the latest variable and function values for the contract
# Every time we run our deploy.py file we are creating a new contract and then also making a state change to the contract
# In this file, all we're doing is calling the blockchain for the latest states
# So we're calling the retrieve function for the latest "favoriteNumber" and we're also checking to see how many contracts we've deployed in the project and then we're printing out the addresses of the first few contracts if they exist (if we haven't deployed at least 3 contracts in this project, then we'll get an error)
def read_contract():
    simple_storage = SimpleStorage[-1]
    print(simple_storage.retrieve())
    print(len(SimpleStorage))
    print(SimpleStorage[0])
    print(SimpleStorage[1])
    print(SimpleStorage[2])


def main():
    read_contract()