pragma solidity ^0.8.24;

contract SimpleBlockchain {
    // This contract handles simple blockchain operations, including transfers of balances.
    mapping(address => uint256) public balances;

    event Transfer(address indexed from, address indexed to, uint256 value);

    function transfer(address to, uint256 value) external {
        // This function transfers a specified value from the sender's balance to the recipient's balance.
        require(balances[msg.sender] >= value, "Saldo insuficiente");
        balances[msg.sender] -= value;
        balances[to] += value;
        emit Transfer(msg.sender, to, value);
    }
}
