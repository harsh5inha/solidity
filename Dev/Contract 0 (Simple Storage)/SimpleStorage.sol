// SPDX-License-Identifier: MIT


// Need to specify which version we want to work with
pragma solidity ^0.6.0;

// init a contract named SimpleStorage
contract SimpleStorage {

    // init a number
    // technically variables are just functions that call themselves. So we could either not specify 
    // anything, in which case it would be an internal function and so we wouldn't be able to 
    // interact with it outside this contract or we specify it as a public function and we are able to 
    // interact with it outside this contract
    // this will get initialized to 0
    uint256 public favoriteNumber;


    // init a bool
    bool public favoriteBool;

    // init a struct to create people
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // init an array whose elements are instances of the `People` struct.
    // Also it's public
    People[] public people;


    // init a mapping called nameToFavoriteNumber that maps names to integers. Kind of like a hash table.
    mapping(string => uint256) public nameToFavoriteNumber;

    // create a function that is public (so can be accessed outside this contract) and sets favoriteNumber
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    // init a function that just pulls the state of favoriteNumber
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    // init a function called addPerson which takes in a name and a number
    // adds them in to the people array, and adds the pairing to the nameToFavoriteNumber dictionary
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

}


// We linked the above up to the Rinkeby test net and deployed and it did indeed get added to the chain
// with transaction hash 0xfc6318d98ef964440627180ee24ad982ffcb5857ac964f355eff67ccb1ed0287