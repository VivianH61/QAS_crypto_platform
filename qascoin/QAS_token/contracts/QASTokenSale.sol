// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

import "./QASToken.sol";

contract QASTokenSale {
	address admin; // admin is not public since we do not want to expose the address of the admin
	QASToken public tokenContract;
	uint256 public tokenPrice;
	uint256 public tokensSold;
	event Sell(address _buyer, uint256 _amount);

	constructor (QASToken _tokenConctract, uint256 _tokenPrice) public {
		// Assign an admin
		admin = msg.sender;
		// Token Contract - we want actually purchase the token
		tokenContract = _tokenConctract;
		// Token Price
		tokenPrice = _tokenPrice;
	}

	// safe multiply ==> from dapphub/ds-math
	function multiply(uint x, uint y) internal pure returns (uint z) {
		require(y == 0 || (z = x * y) / y == x);
	}

	// Buy Tokens
	function buyTokens(uint256 _numberOfTokens) public payable {
		
		// Require that value is equal to tokens
		require(msg.value == multiply(_numberOfTokens, tokenPrice)); // msg.value is the amount of wei we are sending
		// Require that the contract has enough tokens
		require(tokenContract.balanceOf(address(this)) >= _numberOfTokens); // use address(this) not this here
		// Require that a transfer is successful
		require(tokenContract.transfer(msg.sender, _numberOfTokens));

		// Keep track of tokensSold
		tokensSold += _numberOfTokens;
		// Trigger Sell Event
		emit Sell(msg.sender, _numberOfTokens);
	}

	// Ending Token Sale
	function endSale() public {
		// Require admin
		require(msg.sender == admin);
		// Transfer remaining QAS token to admin
		require(tokenContract.transfer(admin, tokenContract.balanceOf(address(this))));
		// transfer the balance to the admin
		payable(admin).transfer(address(this).balance);
	}

}