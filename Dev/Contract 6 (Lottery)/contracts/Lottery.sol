pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

// Inheriting ownable modifier functionality from the OpenZeppelin dependency, also VRFConsumerBase
contract Lottery is VRFConsumerBase, Ownable {

    // Declare a bunch of variables
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED, 
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    // Here we have our constructor, and also a sub-constructor for the VRFConsumerBase
    // We pass in _priceFeedAddress as the address from where we'll pull the ETH/USD conversion
    // We pass in _vrfcoordinator as the address of the contract from where we'll verify that the returned number from the chainlink node is truly random.
    // We pass in _link as the address of the Chainlink token used as the payment to the node for its services.
    // We pass in _fee as how much we're going to pay to the chainlink node for its services.
    // We pass in _keyhash as the address of the chainlink node we're going to use.
    constructor(
        address _priceFeedAddress, 
        address _vrfCoordinator, 
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        // lottery_state = 1 (this is equivalent to the below)
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    
    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        // $50 minimum
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        players.push(msg.sender);
    }


    function getEntranceFee() public view returns (uint256) {
        (, int256 price,,,) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        // 50 * 1,000,000,000,000,000,000 / ~$3,000 (ETH price)
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED, "Can't start a new lottery yet.");
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee); // can only call this function if this contract has some chainlink token. So need to make sure you send the contract some token before trying to end the lottery.
        emit RequestedRandomness(requestId); // this will emit the requestId to our transaction on chain, which will help us in our unit test to make sure that the endLottery() function is working as expected
    }

    // We use "override" to override the initial definition of the fulfillRandomness function
    // This is the response function from the above function. So when we call endLottery() the Chainlink oracle will 
    // send back this function
    // Below we are saying, let's get a random number from Chainlink, then use it to pick one of the addresses which deposited 
    // into the contract, then transfer them the whole balance of the account, reset the players array, and close the lottery
    // However if we're running this on a local ganache chain, there won't actually be a chainlink node to call the fulfillRandomness function, so this will end with nothing 
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER,"You aren't there yet!");
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}