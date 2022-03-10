from scripts.helpful_scripts import get_account
from brownie import OurToken
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")

def deploy_contract():
    account = get_account()
    ourtoken = OurToken.deploy(
        initial_supply,
        {"from": account}
    )
    return ourtoken




def main():
    deploy_contract()