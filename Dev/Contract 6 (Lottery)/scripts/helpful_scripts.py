from brownie import network, config, accounts, MockV3Aggregator, VRFCoordinatorMock, Contract, LinkToken
from web3 import Web3

# Here we are categorizing networks 
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

# These are parameters requiered by the Mock smart contract we're using from chainlink
DECIMALS = 8
STARTING_PRICE = 200000000000

# Below we're saying, use a package generated account unless we're deploying to a live chain, in which case use our actual private key
def get_account(index=None, id=None):
    if index: 
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

# This is just a mapping of terms to deployed contracts
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken}

# Below we're saying deploy all three of our mock contracts. One to simulate a local USD/ETH priceFeed, one to simulate 
def deploy_mocks(decimals=DECIMALS, starting_price=STARTING_PRICE):
    MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    link_token = LinkToken.deploy({"from": get_account()}) # need to set it to link_token because we're using it below
    VRFCoordinatorMock.deploy(link_token.address, {"from":get_account()}) 
    print("Mocks Deployed!")

# Below we're saying, if we're on a local chain then deploy the mock contract if it hasn't been deployed and return the contract. If it has been deployed already, then just return the latest deployment
# But if we're on a live chain or a locally forked real chain, then we return the contract from the chain (address stored in our config)
def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # using the contract package to derive the contract from its ABI
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract

# Below we're saying send the lottery smart contract 0.25 Link Tokens from this address. It will need the link when it makes a request 
# for the random number from the oracle
def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token") # this will return a contract, but that's what a token actually is. It's a smart contract. But if we're on a live net, then we'll have to use real tokens, so we'll need to make sure our account has the needed tokens to send to the contract. Which then sends those tokens to the oracle in exchange for a random number.
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract!")
    return tx