// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // Using our contract's constructor, and the ERC721 contract constructor, passing in name 
    // and symbol (inputs needed for ERC721 contract constructor)
    constructor () public ERC721 ("Doggy","DOG"){
        tokenCounter = 0;
    }

    // This function, when called, basically initializes a mapping of msg.sender to a new tokenID
    // And it stores a mapping of the tokenID to the tokenURI that msg.sender provides
    // So the "NFT" is just the contract. And the collection is the mappings stored on the contract
    // So functionally, this NFT will store the mapping of which address owns which tokenID and 
    // which tokenIDs map to which tokenURIs and from the output of the URI, which tokenURIs map to which imageURIs
    function createCollectible(string memory tokenURI) public returns (uint256){
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId); // maps msg.sender to tokenID
        _setTokenURI(newTokenId, tokenURI); // Maps tokenID to tokenURI
        tokenCounter = tokenCounter + 1; // increment so the next token we mint will have a unique ID
        return newTokenId; 
    }
}