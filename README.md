# Blockchain & Solidity Full Course (Python based)

[YouTube Video](https://www.youtube.com/watch?v=M576WGiDBdQ)

Master GitHub Table of Contents: https://github.com/smartcontractkit/full-blockchain-solidity-course-py#non-technical-explainer


File Structure:

- Resources is a file with a few helpful things
- `High Level Thoughts` is a doc that goes over my high level takeaways of what I've learned from teh crypto space.
- `todo` is a doc that has some future crypto areas that would be interesting to look into.
- `Dev` is the primary folder. Each folder has a project.
- We have 12 contracts within `Dev`.
    Contracts 0-2 are basically just solidity files that don't have a deployment script
    Contracts 3-9 are fully fledged contracts that can be deployed to a local Ganache Chain or to a local test net or even to the live ETH chain if we wanted.
    Contracts 10 & 11 are not completed. I stopped doing the course fully and instead opted to just watch and skim the lectures from this point because I felt like I got the gist of crypto and because actually implementing the projects takes quite a while. I understand all the information though conceptually.

Explanaition of Projects
- Contract 0 (Simple Storage) - Lesson 1. This is just a basic framework for a contract.
- Contract 1 (Storage Factory) - Lesson 2. This is a framework for contract inheritance and how to interact with variables and attributes of already deployed contracts.
- Contract 2 (Fund Me) - Lesson 3. This shows us how we can create a smart contract that can accept payment from others and deposit those payments into the contract creator's address and only that address.
- Contract 3 (Python Simple Storage) - Lesson 4. This project deploys a contract to the Rinkeby chain, checks the value of a variable, updates that value through another transaction, and then checks the value again.
- Contract 4 (Brownie Simple Storage) - Lesson 5. This project does the same as the above, but using the Brownie package, thus waaay fewer lines of code needed.
- Contract 5 (Brownie Fund Me) - Lesson 6. This project recreates Contract 2, except using Brownie, and it can actually be deployed to testnets, live nets, local forks, etc. Anyone can deposit to an address, but only the owner can withdraw.
- Contract 6 (Lottery) - Lesson 7 & Lesson 8. This project creates a lottery such that anyone can deposit at least $50 worth of ETH, then the lottery creator can end the lottery whenever they want and an account will get picked at random. We use ChainLink's VRF coordinator to generate the random number, so it's all still decentralized.
- Contract 7 (ERC20) - Lesson 9. In this contract we are deploying 1000 basic ERC tokens called "ourtoken" with symbol OT. We aren't actually writing out all the code to create an ERC20 token, we're just pulling the code from the zeppelin repository through inheritance. Tokens can be deployed either to a test net or to a local chain, the code is robust to either. 
- Contract 8 (AAVE) - Lesson 10. This app is really just kicking the tires to make sure we can wrap our ETH, deposit it on to AAVE (a lending platform), borrow some DAI using that wETH as collateral from them, and then give AAVE back the DAI to get our wETH back. The app is robust to a local fork of the ETH mainnet and the live Kovan testnet. But we could add more chains by just extending our config file appropriately. 
- Contract 9 (NFTs) - Lesson 11. This project deploys some NFTs, hosted on IPFS. We can either host our own IPFS node, or we can go through Piñata, a third party pinning service. We can deploy multiple tokens to our collectible. The images are pixelated dogs. We have several scripts for this project, some to create the metadata, some to deploy, etc.
- Contract 10 (Upgrades) - Lesson 12. We didn't actually do this project because I started to feel like I was getting th hang of crypto at this point and the projects were taking a long time. But I skimmed the lectures etc. If we had done this project, we would've walked through how to deploy an implementation contract called a "box", a proxy contract, and then a new implementation contract. We'd then have the proxy point to the new implementation contract instead of the first one. Basically, it walks us through how to deal with contract "upgrades".
- Contract 11 (Full Stack Defi) - Lesson 13. Lesson 14. Similar to the above, we didn't actually do this project because it would have taken so long. Proabbly a couple days. But we did skim the lesson. It walks us through first creating the back end functionality of allowing users to stake particular tokens on our contract, etc. But it also walks us through how to create an attractive front end for the users to interact with. From pop up boxes to background colors, etc. All the important stuff. It's been great to see an end to end product come together. In the future, I might come back to this lesson and actually do the project end to end. I think it'd help build some muscle memory for React Development. The Web3 aspect of this stuff now actually seems relatively simple lol.


Steps to create a project:
1. get brownie set up etc
2. `brownie init`
3. `brownie compile` within a directory to turn our solidity files into 

To check the networks available in brownie we do `brownie networks list`
To test on a particular network we do `brownie test --network {network name}` so for example `brownie test --network mainnet-fork-dev`