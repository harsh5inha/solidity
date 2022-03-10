from brownie import network, config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1
AMOUNT = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    # we get some weth when on a local chain bc brownie will reset our accounts every time. But in the real world, 
    # we prob won't need to get some weth every time, bc we might already have some
    if network.show_active() in ["mainnet-fork-dev"]: 
        get_weth()
    lending_pool = get_lending_pool()

    # Approve that we want to send our ERC20 token
    # Below we're allowing the lending ppol contract to withdraw 0.1 WETH from our account
    # In plain English, we're signing off on AAVE to collect our WETH
    approve_tx = approve_erc20(AMOUNT, lending_pool.address, erc20_address, account)
    print("Depositing...")

    # Now we can just use the deposit function of the lending_pool contract to actually deposit 
    # our WETH to AAVE (The 0 input is for the refferral code, but that's been deprecated)
    tx = lending_pool.deposit(erc20_address, AMOUNT, account.address, 0, {"from": account})
    tx.wait(1)
    print("Deposited!")
    
    # Here we're calling the get_borrowable_data() function that we defined below to 
    # return the amount we can borrow and how much we owe to the AAVE platform
    borrowable_eth, total_debt = get_borrowable_data(lending_pool, account)
    print("Let's borrow!")

    # Below we're pulling the DAI to ETH price conversion via the Chainlink Oracle contract
    # Then we're specifying that we're going to borrow 95% of the maximum DAI that we're allowed to borrow from the platform
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # Below we're calling the borrow() function of the lendingPool contract to request to borrow the above amount of DAI 
    # from the AAVE platform. The DAI will be transferred to our address
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI!")

    # below we're printing out how much ETH we can borrow and how much we've borrowed in total,
    # then we're repaying all of the DAI that we borrowed from the platform
    # And then we're printing out the amount of ETH we have deposited and the amount of DAI we have borrowed in total again
    get_borrowable_data(lending_pool, account)
    # repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    get_borrowable_data(lending_pool, account)
    print("You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!")


# Below we're defining a function, that when called, will approve a lendingPool address to withdraw a specified amount 
# of our DAI tokens and then call the repay() funciton of the lendingPool contract which then sends the specified amount
# of DAI back from the account's wallet to AAVE
def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)

    print("Repaid!")


# Below we're applying the AggregatorV3Interface Interface to a price feed contract address
# When we implement it above, we're specifying the DAI/ETH conversion, but technically this function 
# could be used for any price feed contract
def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)



# Below we're calling the getUserAccountData() function of the LendingPool contract to return all the 
# financial information of the account on the AAVE platform, and we're printing a few pieces of information out, 
# like our current amount deposited, borrowed, and available to borrow
def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))


# Below we're defining a way to approve sending ERC20 tokens to another address. Technically, we're giving 
# permission to another address to withdraw a certain amount of tokens from msg.sender
def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx


# The lending pool is the contract address that is the primary way we interface with AAVE. 
# On that contract we can call deposit(), withdraw(), etc. to interact with their app
# however the address could change (different markets etc) so we actually need to work with the LendingPoolAddressesProvider
# contract, which will direct us to the most updated contract to work with

# So what we're doing below is we're applying the LendingPoolAddressesProvider Interface on the contract address, which 
# enables us to interact with the contract, and then we're calling the getLendingPool() function on that address, which 
# is defined in the contract, to pull the address of the actual contract that we should use to interact with AAVE
# And on that contract address we're initiating a LendingPool interface so we can interact with the contract 
# And then we're returning that contract 
def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
