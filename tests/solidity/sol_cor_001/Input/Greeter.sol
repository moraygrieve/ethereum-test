// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;

contract Greeter {
    string public greeting;

    constructor() {
        greeting = "Hello World";
    }

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string memory) {
        return greeting;
    }
}