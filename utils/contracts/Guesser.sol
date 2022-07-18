// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;

contract Guesser {
    address public owner;
    uint256 public number;

    constructor(uint256 _initialNumber) {
        owner = msg.sender;
        number=_initialNumber;
    }

    function guess(uint256 i) view public returns (int) {
        if (i<number) return 1;
        if (i>number) return -1;
        return 0;
    }

    function destroy() public {
        require(msg.sender == owner, "You are not the owner");
        selfdestruct(payable(address(this)));
    }
}