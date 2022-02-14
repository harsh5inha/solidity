# accounts package helps us with accounts, creates 10 acounts if using a test Ganache chain etc.
# config helps us interact with the brownie-config.yaml file
# netowrk helps us interact with live networks etc.
from brownie import accounts, config, SimpleStorage, network

# this code basically 
# 1. grabs our account number
# 2. deploys the contract we defined in SimpleStorage.sol to the rinkeby blockchain
# 3. prints out the initial value of the favoriteNumber variable
# 4. updates the value to 15 in a new transaction to the blockchain
# 5. And then calls the variable again to see the updated value
def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


# if using a test Ganache chain, then use the first account address they give us
# else use the private key we stored in our environment variables
def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()