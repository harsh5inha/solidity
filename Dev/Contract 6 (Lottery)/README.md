In this contract, we create a lottery smart contract. Users can enter the lottery by sending 
in some ETH (in this case at least $50 worth). There is no limit to how many people can enter 
the lottery. However the lottery has to be started in order to enter. It can only be started 
by the contract creator, and it can only be ended by the contract creator. When the lottery is
ended, a random winner is selected and all the deposited funds go to the winner. 

To randomly pick a winner, we're using the Chainlink VRF contract to generate a random number. 
In order to do this, we need to pay chainlink some oracle gas. In this case, we have to pay them 
some LINK token. We do this via the lottery contract, so when it comes time to end the lottery, 
we make sure to fund the lottery contract with .1 LINK. 

This contract can be deployed on any local or live ETH net. The code is robust to local testing 
but also deployement to a live network.


FILE STRUCTURE 

1. CONTRACTS
        A. Lottery.sol:  This is our primary lottery contract.

        B. test/MockV3Aggregator.sol:   This contract is a mock smart contract to get the ETH/USD conversion rate 
                                        from an oracle. We create it in case we want to test our Lottery 
                                        contract in a local chain (but not a local fork of a mainnet). Without it, 
                                        we wouldn't be able to pull the ETH/USD conversion because local chains won't 
                                        have that information stored on chain. Unless we fork a mainnet or 
                                        something, in which case we wouldn't need to use this mock contract.
        
        C. test/VRFCoordinator.sol: This contract is a mock smart contract that acts as a chainlink node that 
                                    will check to see if the returned random number is indeed random. 

        D. test/LinkToken.sol:  This contract is a ERC677 token. It's LINK token. We have a mock of it here 
                                in case we want to test our lottery contract in a local chain (but not a local 
                                fork of a mainnet).

 
2. SCRIPTS 
        A. helpful_scripts.py:  This file lists out a few functions that are used elsewhere in the app including 
                                get_account(), get_contract(), fund_with_link(), and deploy_mocks(). 

        B. deploy_lottery.py:   This file runs through how exactly we'd go about deploying our smart contracts to 
                                a chain and then interacting with our three main functions: start, enter, end.

3. TESTS

        A. test_lottery_unit.py:    This file tests whether most of our key functions are working in our lottery 
                                    contract.

        B. test_lottery_integration.py: This file tests whether the lottery contract works at large.

4. CONFIG 

        A. brownie-config.yaml: This file lays out the addresses of various smart contracts and oracles and keyhashes 
                                that we should be using for different chains. We also specify whether we should be publishing 
                                the source code of our contracts depending on the specific chain. We're also telling brownie 
                                where to pull the chainlink packages from.


To run this app on a dev network:
`brownie run scripts/deploy_lottery.py`

And on Rinkeby:
`brownie run scripts/deploy_lottery.py --network rinkeby`

You can check the contract we deployed on rinkeby here:
`0x2e3FC57Bf7065410371207b963c9DEb7D27f849A`

But of course every time you deploy this contract, you'll get a new address that you can check.