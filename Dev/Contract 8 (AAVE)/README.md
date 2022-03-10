In this app, we're working with AAVE, a borrowing and lending platform. We first work 
directly with the wETH contract to swap some ETH for some wrapped ETH, and then we 
deposit .1 of that wETH on to the AAVE platform. We then figure out how much DAI 
we can borrow fromt eh platform using that deposited wETH as collatoral, and we 
borrow 95% of that total. We get the price conversion from Chainlink. Then we return 
that same amount of DAI back to the platform.

This app is robust to a local fork of the ETH mainnet and the live Kovan testnet. But 
we could add more chains by just extending our config file appropriately. 

We only swap ETH for wETH if we're deploying to the local fork of the mainnet. If we're 
deploying to Kovan, then we don't swap for wETH because presumably, our live address 
will already have some. Though of course, we could always just add in the functionality 
by adjusting line 12 in aave_borrow.py. 

So this app is really just kicking the tires to make sure we can wrap our ETH, deposit it 
on to AAVE, borrow some DAI using that ETH as collatral, and then give them back the DAI.


FILE STRUCTURE

1. INTERFACES
    A. AggregatorV3Interface - An interface that we use to grab the chainlink price feed conversions
    B. IERC20 - An interface that we use to interact with ERC20 tokens (wETH and DAI in this app)
    C. ILendingPool - An interface that we use to interact with the lendingPool contract on AAVE
    D. ILendingPoolAddresses - An interface that we use to interact with the LendginPoolAddresses cotnract via AAVE
    E. IWeth - An interface that we use to interact with the wETH contract 
2. Scripts
    A. aave_borrow.py - This is the main file that does everything
    B. get_weth.py - This file defines how to exchange our ETH for wETH
    C. helpful_scripts.py - This one tells us how to grab an account
3. Tests
    A. test_aave_borrow.py - This one is just testing all the normal basic stuff
4. Config
    A. This file is important! Make sure you know where all those addresses are coming from and why and when you're pulling from them in the app.

To run:
`brownie run scripts/aave_borrow.py --network kovan`
`brownie run scripts/aave_borrow.py --network mainnet-fork-dev`