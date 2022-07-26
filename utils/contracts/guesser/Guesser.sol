// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;

contract Guesser {
    uint256 public number = 12;

    function guess(uint256 i) view public returns (int) {
        if (i<number) return 1;
        if (i>number) return -1;
        return 0;
    }
}