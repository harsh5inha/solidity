from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time 

# Below we're saying deploy our lottery contract, passing in three addresses. One for the ETH/USD conversion, one for the Chainlink 
# random number number verification contract, and one for the chainlink token contract (all mock addresses if we're on a local chain)
# Also we pass in the fee (amount of tokens to be sent to the chainlink node), and the keyhash of the oracle node that we're using 
# to get the random number.
def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False)
    )
    return lottery # added this in later which ended up making my test scripts pass, earlier they weren't working

    print("Deployed Lottery!")

# Below we're saying make the lottery state OPEN from CLOSED
def start_lottery():
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from":get_account()})
    starting_tx.wait(1) # need to do this bc sometimes the code trips over itself if the above line doesn't fully execute before the below line does
    print("The lottery is started!")

# Below we're saying enter this user in to the lottery with the below amount of ETH
def enter_lottery():
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from":get_account(), "value":value})
    tx.wait(1)
    print("You entered the lottery!")

# Below we are ending the lottery. Which means we send the lottery contract some link tokens, then in the lottery contract we 
# send the tokens to the Chainlink Oracle and then wait a few blocks for the oracle to return the random number we requested
def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(180) # we need to wait because the oracle needs time to respond with the random number. This will happen in subsequent blocks. This is the request and respond model discussed earlier.
    print(f"{lottery.recentWinner()} is the new winner!") # after a while, the fulfillRandomness() funciton will have been called automatically, and so the winner would have been selected and teh lottery closed.





def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()