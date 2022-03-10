In this contract we are deploying 1000 basic ERC tokens called "ourtoken" with symbol OT. 
We aren't actually writing out all the code to create an ERC20 token, we're just pulling 
the code from the zeppelin repository through inheritance. Tokens can be deployed either 
to a test net or to a local chain, the code is robust to either. 


FILE STRUCTURE 

1. CONTRACTS
        A. OurToken.sol:  This is our primary ERC20 contract.
 
2. SCRIPTS 
        A. helpful_scripts.py:  This file lists out the get_account() function which we use elsewhere in the app. 

        B. deploy.py:           This file deploys our tokens to a chain.


If we wanted to check how much OurToken a particular acocunt has, we'd do:
`OurToken.balanceOf(deployerAddress)`

To transfer some of those tokens to another address we could do: 
`OurToken.transfer(otherAddress, amount)`

These methods are built in to the ERC20 standard, which is what makes these tokens so easy 
to work with. 