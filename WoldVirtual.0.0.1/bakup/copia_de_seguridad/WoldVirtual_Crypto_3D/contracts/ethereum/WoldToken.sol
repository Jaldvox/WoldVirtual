// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Snapshot.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title WoldToken
 * @dev Token principal del metaverso en Ethereum
 */
contract WoldToken is ERC20, ERC20Burnable, ERC20Snapshot, Ownable, Pausable {
    // Eventos
    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);
    event SnapshotCreated(uint256 id);
    event Paused(address account);
    event Unpaused(address account);

    // Constructor
    constructor() ERC20("Wold Virtual Token", "WOLD") Ownable(msg.sender) {
        _mint(msg.sender, 1000000000 * 10 ** decimals()); // 1 billón de tokens
    }

    // Funciones principales
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
        emit TokensMinted(to, amount);
    }

    function burn(uint256 amount) public override {
        _burn(msg.sender, amount);
        emit TokensBurned(msg.sender, amount);
    }

    function snapshot() public onlyOwner {
        _snapshot();
        emit SnapshotCreated(_getCurrentSnapshotId());
    }

    function pause() public onlyOwner {
        _pause();
        emit Paused(msg.sender);
    }

    function unpause() public onlyOwner {
        _unpause();
        emit Unpaused(msg.sender);
    }

    // Funciones internas
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Snapshot) whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
} 