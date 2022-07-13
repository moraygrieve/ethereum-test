// SPDX-License-Identifier: MIT
pragma solidity 0.8.15;

contract Greeter {
    int public value;

    constructor() {
        value=12;
    }

    function guess(int i) view public returns (int) {
        if (i<value) return 1;
        if (i>value) return -1;
        return 0;
    }
}