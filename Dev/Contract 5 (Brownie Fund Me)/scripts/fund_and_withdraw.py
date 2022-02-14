from brownie import FundMe
from scripts.helpful_scripts import get_account

# Here we're getting the entrance fee from the most recently deployed contract and then running the func function of the account to deposit the entrance fee + 100 into the contract
def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getEntranceFee() + 100
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding")
    fund_me.fund({"from": account, "value": entrance_fee})

# Here we're just withdrawing the funds from the most recent contract to the creator's account
def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()