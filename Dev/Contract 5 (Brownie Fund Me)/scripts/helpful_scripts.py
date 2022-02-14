from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

# Here we are categorizing networks 
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# These are parameters requiered by the Mock smart contract we're using from chainlink
DECIMALS = 8
STARTING_PRICE = 200000000000

# Here we're using a package generated account if the chain we're deploying to is one of the above (read: not a live chain)
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    # If it's not one of the above chains, then let's set the account as our private key
    else:
        return accounts.add(config["wallets"]["from_key"])

# If we haven't deployed the mock contract yet, then let's deploy it with the parameters. If we have, then do nothing.
def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")