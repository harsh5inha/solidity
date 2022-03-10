HOW TO DEPLOY

So first we do `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`
which deploys our NFT contract to the Rinkeby chain, verifies it, and mints one token (but doesn't yet have the mapping from tokenID to tokenURI).

Then after a few minutes we do `brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby`. This uploads the correct dog picture to IPFS (which dog picture exactly is picked under the hood in the step above) and creates the metadata for the token and uploads the metadata to IPFS as well and also stores the metadata locally.

Then we can do `brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby`. This mints another token to the contract. So now we have two tokens in the collection (same NFT contract). 

Then we do `brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby` again to once again upload the image and create and upload the metadata for the second token on the contract.

Then we do `brownie run scripts/advanced_collectible/set_tokenuri.py --network rinkeby`. This is going to finally go in to our NFT contract, and map the tokens to their respective tokenURIs. Those URIs will have all the metadata we created above on IPFS and will have an imageURI included as part of the metadata. And that imageURI will return the image we uploaded earlier on IPFS as well. 

Then we can go to Opensea and look up our NFT contract address and we'll see our NFTs! Because Opensea knows how to pull in the images and metadata from IPFS for any ERC721s deployed on Rinkeby (or mainnet as well obv).

If you can't see your NFTs, check your tokenURI and imageURI outputted from the create_metadata.py file. Make sure they're loading the expected output. If not, it could be because your IPFS node isn't active anymore. So you'll have to spin that up again in a separate terminal window by doing `ipfs daemon`. OR if you're hosting on IPFS via Pinata or something then that shouldn't be an issue. 

If you still can't see it, then request OpenSea to refresh the metadata. Should take a minute and then you'll be able to see it so long as the contract is deployed to the chain, the tokenURI is valid, and the imageURI is valid.



FILE STRUCTURE

1. CONTRACTS
    A. LinkToken.sol - This contract is a mock of the Chainlink Token. We need it in case we decide to request a random number from the VRFCoordinator on a local chain. (We need to pay the VRFCoordinator some link for thir services.)

    B. VRFCoordinatorMock.sol - This is a mock contract to simulate the VRFCoordinator which gives us back a decentralized random number. We use this when we are deploying to a local chain that doesn't have the VRFCoordinator smar contract stored on chain.

    C. AdvancedCollectible.sol - This is an NFT contract (ERC721). It's called Dogie, with symbol DOG. It has a createCollectible() function which, when called, requests a random number from Chainlink to pick one of our three dog pictures at random and then mints a new token for the msg.sender (there's no tokenURI yet though). However we do store which dog picture the token should map to. When the setTokenURI() function is called, we map the tokenID to the inputted tokenURI (however only the token owner is able to call this functin). So to summarize, when we deploy this contract, we deploy an NFT contract. And then we have two functions stored on contract which can be called in conjunction to pick one of our three dog images at random and mint a token which can be claimed by the user (and only the user) which corresponds to that image and metadata on IPFS, if we have our own IPFS node spun up. If not we can use the upload_to_pinata.py script to get our image and metadata pinned to IPFS by Pinata (a third party).

    D. SimpleCollectible.sol - This is an NFT contract (ERC721). It's called Doggy, with symbol DOG. It has a createCollectible() funciton which, when called, mints a token 
    for the caller and sets the tokenURI to whatever they input when calling the function.

2. IMG
    A-C. Three locally stored images of dogs. Nothing crazy here.

3. METADATA
    A. Rinkeby folder - This folder stores the metadata for each token locally (it's all uploaded to IPFS as well).

    B. sample_metadata.py - This is a template for our token metadata.

4. SCRIPTS
    A. simple_collectible/deploy_and_create.py - When we run this file, we deploy our SimpleCollectible NFT contract and mint a token for the msg.sender. We provide a manual tokenURI (which includes the imageURI internally). We also provide a link to view the NFT on OpenSea if we deploy to Rinkeby since Opensea is able to pull the metadata and image from chain and automatically creates a URL to display all NFTs 
    based on the contract address. To run this file we do:
    `brownie run scripts/simple_collectible/deploy_and_create.py --network rinkeby`

    B. advanced_collectible
        1. create_collectible.py - When we run this file, we grab the latest advancedCollectible NFT contract we deployed, fund it with 0.1 LINK, and then call the createCollectible() function on the contract, which picks a random dog breed and mints a new token for the msg.sender (but the token lacks a tokenURI for now so it doesn't yet map to actual metadata/image yet). So this is basically the same as deploy_and_create.py, except it doesn't deploy a new contract. It just mints new tokens in a collection for the last contract we deployd. To run this file we do:
        `brownie run scripts/advanced_collectible/create_collectible.py --network rinkeby`

        2. create_metadata.py - When we run this file, we deploy the associated image and metadata for each token on our last deployed NFT contract to IPFS. (We also store the metadata for each token locally.) So the metadata for all the tokens on the contract are all assembled and deployed to IPFS. As are the associated images. All that's left is to  link up the token to tokenURI (which we do in set_tokenuri.py). To run this file we do:
        `brownie run scripts/advanced_collectible/create_metadata.py --network rinkeby`

        3. deploy_and_create.py - When we run this file, we deploy our AdvancedCollectible NFT contract, fund the contract with 0.1 LINK so that it can pay the VRFCoordinator node for a random number, and call the createCollectible() function on the contract, which picks a random dog breed and mints a new token for the msg.sender (but the token lacks a tokenURI for now so it doesn't yet map to actual metadata/image yet). To run this file we do:
        `brownie run scripts/advanced_collectible/deploy_and_create.py --network rinkeby`

        4. set_tokenuri.py - When we run this file we call the setTokenURI() function from the 
        AdvancedCollectible contract for each token, which basically creates the mapping for each token to its tokenURI on IPFS. We also provide a link to view the NFTs on OpenSea if we deploy to Rinkeby since Opensea is able to pull the metadata and image from chain and automatically creates a URL to display all NFTs based on the contract address. To run this file we do:
        `brownie run scripts/advanced_collectible/set_tokenuri.py --network rinkeby`

    C. helpful_scripts.py - This file defines a bunch of useful functions and variables that we pull in to other scripts in this project. get_account, get_contract, deploy_mocks(), etc.

    D. upload_to_pinata.py - This script basically demonstrates how we'd go about sending an image to Pinata (a 3rd party IPFS management system) so they can pin the image on IPFS so that we don't have to keep an IPFS node running on our local machine to host an image on IPFS. To run this file we do:
    `brownie run scripts/upload_to_pinata.py --network rinkeby`


5. TESTS
    A. Integration
        1. test_advanced_collectible_integration.py - normal test stuff

    B. Unit
        1. test_advanced_collectible.py - normal test stuff

        2. test_simple_sollectible.py - normal test stuff






INITIALIZING IPFS
We pulled the IERC721 file from `openzeppelin-contracts@4.5.1/contracts/token/ERC721/ERC721.sol` on Github.
So we copy and pasted the ERC721 standard and defined it as an interface. 


For this contract, we needed to interact with IPFS (primarily the `/api/v0/add` API endpoint to upload our files) so we downloaded the command line tool for IPFS. So we did: 
`curl -O https://dist.ipfs.io/go-ipfs/v0.11.0/go-ipfs_v0.11.0_darwin-amd64.tar.gz`
`tar -xvzf go-ipfs_v0.11.0_darwin-amd64.tar.gz`
`cd go-ipfs`
`bash install.sh`
`ipfs --version`

Then to initialize our computer as a node we did:
`ipfs init`

That set up the IPFS directory and settings files etc. It also gave us a peer identity, 
which is our node’s ID. Other nodes on the network use it to find and connect to
us. We can run `ipfs id` at any time to get it again if we need it. Our peer identity is 
`peer identity: 12D3KooWLSkYCVYrqSXsg8wwyyeAiVgoViWs9rBNRGLYKDRjigG5`

It will also give us a command to run to get started. For us it was: 
`ipfs cat /ipfs/QmQPeNsJPyVWPFDVHb77w8G42Fvo15z4bG2X8D2GhfbSXc/readme`

After running this we get a welcome message saying that we're interacting with IPFS. 
Then to take our node online (run our own IPFS node) we do:
`ipfs daemon`

It'll output a bunch of stuff and will give us a WebUI, which is basically the 
address for our IPFS URL. And now our copmuter is running an IPFS node!

The way it works is that if we dploy our images to our IPFS node, then our images 
will be hosted there. But if we decide to stop running our node (end the daemon process)
then the image won't be able to be found unless someone else pins your image to their 
node (hence the pseudo decentralization). So people also upload their images to Pinata, 
a third party IPFS file management service, they'll pin whatever we have in our node.