// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract (by calling the fund function)
// Only the owner of the contract can withdraw the ETH (by just calling the withdraw function)



pragma solidity >=0.6.6 <0.9.0;

// Get the latest ETH/USD price from chainlink price feed
// This is getting pulled from the npm package. Basically it's just like importing a package. 
// We're hooking up to the Chainlink oracle here so that we can get the price of Ethereum in dollars from a aseparate decentralized process
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

// This import helps us prevent integer overflow. But we don't really need it if we're using a solidity version above 0.8.
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
	// safe math library check uint256 for integer overflows
    using SafeMathChainlink for uint256;
    
    // disctionary to store which address depositeded how much ETH
    mapping(address => uint256) public addressToAmountFunded;
    // array of addresses who deposited (basically any address which validly called the `fund` function)
    address[] public funders;
    // address of the owner (who deployed the contract) - this is just declaring the variable. We don't actually store anything inside until we 
    // call the constructor, which is called as soon as we deploy
    address public owner;
    
    // the first person to deploy the contract is the owner. A constructor is used only once in a contract and initializes state variables 
    // of a contract, like the owner address
    constructor() public {
        owner = msg.sender;
    }
    
    // create a fund function that is public and obviously payable
    function fund() public payable {
    	// 18 digit number to be compared with donated amount (bc it's in wei)
        uint256 minimumUSD = 50 * 10 ** 18;
        //is the donated amount less than 50USD?
        // Every time you call a function you pass in both a sender and a value, which is where msg.value is coming from here
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        //if not, add to mapping and funders array
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    //function to get the version of the chainlink pricefeed
    function getVersion() public view returns (uint256){
        // Here we are calling the AggregatorV3Interface interface, which we imported at the top of this contract from npm/chaiinlink
        // Which basically is a template of a bunch of functions we can call on other contracts
        // Then we're applying the interface to the contract at the chainlink address they gave us on their website  - 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // And using the functions defiend by the interface on that contract, we're able to grab the version that we're using for the contract (not sure why this matters really, i dont think it has any impact on this contract, just for example I think.)
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        // version() is defined in the interface
        return priceFeed.version();
    }
    
    function getPrice() public view returns(uint256){
        // Here we are calling the AggregatorV3Interface interface, which we imported at the top of this contract from npm/chaiinlink
        // Which basically is a template of a bunch of functions we can call on other contracts
        // Then we're applying the interface to the contract at the chainlink address they gave us on their website  - 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        // And using the functions defiend by the interface on that contract, we're able to grab the ETH/USD conversion
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        // We have a bunch of commas here because latestRoundData() returns like 5 outputs, but we only want the one called answer (the actual price). 
        // So the commas say to skip those outputs.
        // latestRoundData() is defined in the interface
        (,int256 answer,,,) = priceFeed.latestRoundData();
         // ETH/USD rate in 18 digit 
         return uint256(answer * 10000000000);
    }
    
    // 1000000000
    function getConversionRate(uint256 ethAmount) public view returns (uint256){
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        // the actual ETH/USD conversation rate, after adjusting the extra 0s.
        return ethAmountInUsd;
    }
    
    // the modifier here is basically saying like whenever you call this modifier in a function, run this code.
    // SO basically whenever we want to create a function that can only be called by the contract creator, use this modifier.
    // the underscore shows where the funciton should proceed with the rest of its code
    // So like if we placed the underscore before the msg.sender check, then the function would run all its code first, and then run the msg.sender check. Which kind of defeats the purpose of the check
    // modifier: https://medium.com/coinmonks/solidity-tutorial-all-about-modifiers-a86cf81c14cb
    modifier onlyOwner {
    	//is the message sender owner of the contract?
        require(msg.sender == owner);
        _;
    }
    
    // onlyOwner modifer will first check the condition inside it and if true, withdraw function will be executed 
    function withdraw() payable onlyOwner public {
    
  	    // If you are using version eight (v0.8) of chainlink aggregator interface, you will need to change the code below to payable(msg.sender).transfer(address(this).balance);
        msg.sender.transfer(address(this).balance);

        //iterate through all the mappings and make them 0
        //since all the deposited amount has been withdrawn
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    }
}