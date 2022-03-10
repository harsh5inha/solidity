from brownie import accounts, network, config, LinkToken, VRFCoordinatorMock, Contract
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork-dev",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"} # using this so that we can map the random number generated to the breed name when we create our metadata

# Below we're returning the breed name given the randomly generated number.
# We use this function when we generate our metadata in create_metadata.py
def get_breed(breed_number):
    return(BREED_MAPPING[breed_number])


# Below we're saying send the smart contract 0.25 Link Tokens from this address. It 
# will need the link when it makes a request for the random number from the oracle
def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token") # this will return a contract, but that's what a token actually is. It's a smart contract. But if we're on a live net, then we'll have to use real tokens, so we'll need to make sure our account has the needed tokens to send to the contract. Which then sends those tokens to the oracle in exchange for a random number.
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Funded contract!")
    return tx
    


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None

contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}

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
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


# Below we're saying deploy both of our mock contracts. One to simulate a Chainlink token, and one to simulate a VRF Random Number coordinator
def deploy_mocks():
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRFCoordinator deployed to {vrf_coordinator.address}")
    print("Deployed Mocks!")