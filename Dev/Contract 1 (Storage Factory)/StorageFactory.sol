// So in this contract what we're basically doing is creating a way to create these SimpleStorage sub-contracts by just running one function
// and storing them all in an array.
// And we're also showing how to interact with those sub-contracts once they've been initialized. So we write out some functions that can 
// update the variables and attributes of particular sub-contracts which have already been deployed to the chain



// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

// import the SimpleStorage contract we wrote in the other file
import "./SimpleStorage.sol"; 

// init new contract as an instance of the sub-contract
// So this basically makes StorageFactory an instance of SimpleStorage
// So StorageFacotry will have all the functions and variables and arrays of SimpleStorage 
// But it will also have whatever functions and variables we declare here as well
contract StorageFactory is SimpleStorage {
    
    // init an array in which each element is an instance of a SimpleStorage sub-contract itself
    SimpleStorage[] public simpleStorageArray;
    
    // function which, when called, creates a new sub-contract and pushes it to the array
    // what actually gets stored in the array is the address of the contract
    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }
    
    // Using this function basically allow us to add a favorite number to one of the smart contracts we initialized in the array
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // this line finds the SimpleStorage object that is at the address specified and then stores the number as the favorite number of that contract
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber); 
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        // this line finds the SimpleStorage object that is at the address specified and then calls the retrieve function, which displays the favorite number
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve(); 
    }
}