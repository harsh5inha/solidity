from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


# Here we're saying, if the blockchain we're deploying to is not "development" or "ganache-local" then grab the oracle 
# address from our config file 
# (we have two such addresses, one for the Rinkeby testnet and one for the locally forked Ethereum mainnet)
def deploy_fund_me():
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
# Here we're saying, if the blockchain we're deploying to is locally generated then grab the oracle address for the ETH/USD 
# conversion from our Mock oracle contract we set up in MockV3Aggregator
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
# Here we're saying, deploy the contract now, passing in the oracle address as input and publish the source code for 
# verifiction if we specify to do so for this network in our config file (we do this only for the rinkeby test net, because that's the only live chain we've set ourselves up to use in this app)
# Though we could add other chains relatively easily. We'd just need to add in their config info to the config file and add in their oracle address, etc.
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

# This is the address of the smart contract on the Rinkeby chain that pulls the ETH/USD conversion via the chainlink smart contract. We're inputting it here so that it will get passed in as the input of the constructor function, which takes in the desired address