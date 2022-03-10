// contracts/OurToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract OurToken is ERC20 {
    // We're providing 1,000 tokens to start (can be found in our deploy.py file)
    // here we're inputting the name of our token and the symbol. Like for chainlink it'd be Chainlink Token and LINK.
    constructor(uint256 initialSupply) ERC20("OurToken", "OT") { 
        _mint(msg.sender, initialSupply);
    }
}