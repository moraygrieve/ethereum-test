// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC20.sol";

contract OBXCoin is ERC20 {
    constructor() ERC20("OBXToken", "OBX") {
        _mint(msg.sender, 1000000);
    }
}