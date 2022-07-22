// SPDX-License-Identifier: MIT
pragma solidity ^0.8.11;

contract QASToken {

	// Name
	string public name = "QAS Token";
	// Symbol
	string public symbol = "QAST";
	// Standard
	string public standard = "QAS Token v1.0";
	// total supply
	uint256 public totalSupply; // declare the variable with the public function, we do not need to write the getter function for this variable
	
	// event transfer ==> event provide information log
	event Transfer(
		address indexed _from,
		address indexed _to,
		uint256 _value
	);

	// event approve
	event Approval(
		address indexed _owner,
		address indexed _spender,
		uint256 _value
	);

	// balance
	mapping(address => uint256) public balanceOf;

	// allowance
	mapping(address => mapping(address => uint256)) public allowance; // the nested mapping maps the key (the current our address) to any approvals this address has issue no matter which address it is.

	// Constructor
	// Set the total number of tokens
	// Read the total number of tokens
	constructor (uint256 _initialSupply) public {
		balanceOf[msg.sender] = _initialSupply; //msg is a global variable in which sender is the address that call this function which is the default account in this case
		totalSupply = _initialSupply; // total number of tokens // convention to use underscore to represent the variable only available in the local function
		// allocate the initial supply
	}

	// Transfer
	function transfer(address _to, uint256 _value) public returns(bool success) {
		// Exception if account doesn't have enough
		require(balanceOf[msg.sender] >= _value);
		// Return a boolean
		balanceOf[msg.sender] -= _value;
		balanceOf[_to] += _value;
		// Transfer Event
		emit Transfer(msg.sender, _to, _value);
		return true;
	}

	// Delegated Transfser (approve and allowance)
	// approve
	function approve(address _spender, uint256 _value) public returns (bool success) { // approve _spender to spend _value
		// allowance
		allowance[msg.sender][_spender] = _value;

		// approve
		emit Approval(msg.sender, _spender, _value);

		return true;
	}
	// transfer from ==> like the transfer function but for the third party
	function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
		// Require _from has enough tokens
		require(_value <= balanceOf[_from]);
		// Require allowance is big enough
		require(_value <= allowance[_from][msg.sender]);
		// Change the balance
		balanceOf[_from] -= _value;
		balanceOf[_to] += _value;
		// Update the allowance
		allowance[_from][msg.sender] -= _value;
		// Transfer event
		emit Transfer(_from, _to, _value);
		// return a boolean
		return true;
	}

}
