// An NFT Contract
// Where the tokenURI can be one of 3 different dogs
// Randomly selected

// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

// Pulling in the ERC721 standard and the VRFConsumerBase random number contract
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {

    // Declare a bunch of variables, mappings, events
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;  
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    // constructor for all three contracts
    // We pass in _vrfcoordinator as the address of the contract from where we'll verify that the returned number from the chainlink node is truly random.
    // We pass in _linkToken as the address of the Chainlink token used as the payment to the node for its services.
    // We pass in _fee as how much we're going to pay to the chainlink node for its services.
    // We pass in _keyhash as the address of the chainlink node we're going to use.
    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyhash = _keyhash;   
        fee = _fee;          
    }

    // When someone calls the createCollectible() function below, we request a random number.
    // And then under the hood, the fulfillRandomness() function is called (below) 
    // This is based on the request - response function model. And in that function, we pick 
    // a dog breed, map a new TokenID to the breed, and map the sender's  address to the tokenID.
    // So long story short, when we call this function the sender gets minted a new TokenID which 
    // maps to a randomly chosen breed of dog
    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee); // this sends a request for a random number so we can select a random dog breed. This function is defiend in the VRFCoordinator contract.
        requestIdToSender[requestId] = msg.sender; // store mapping in dict
        emit requestedCollectible(requestId, msg.sender); // emit event
    }


    // The function below is called automatically as the response function when the requestRandomness() 
    // function is called from the createCollectible() function above (The code under the hood 
    // can all be found on the VRFCoordinator contract)
    
    // We have to use the requestIdToSender[] dict here because we need to grab the msg.sender 
    // from the createCollectible() function. Not the caller of the fullfillRandomness() function. 
    // Because the caller of fulfillRandomness() is the VRFCoordinator node, not the original
    // msg.sender of the createCollectible() function because this is a response function from 
    // the requestRandomness() function (request - response function model)

    // What this function actually does is explained in the explanation of the createCollectible() function above
    // This is an internal function so that only the VRFCoordinator can call it
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    // This function, when called, sets the tokenURI for a particular tokenID to whatever the caller inputs
    // However, the caller must be the owner of the token to call this function
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved"); // These functions I believe are defined in the ERC721 contract
        _setTokenURI(tokenId, _tokenURI);
    }
}