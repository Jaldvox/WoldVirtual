// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title WoldTokenBSC
 * @dev Token del metaverso en Binance Smart Chain
 */
contract WoldTokenBSC is ERC20, ERC20Burnable, Ownable, Pausable {
    // Eventos
    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);
    event Paused(address account);
    event Unpaused(address account);
    event TaxUpdated(uint256 newTax);
    event TaxCollectorUpdated(address newCollector);

    // Variables
    uint256 public taxRate = 100; // 1%
    address public taxCollector;
    mapping(address => bool) public isExcludedFromTax;

    // Constructor
    constructor(address _taxCollector) ERC20("Wold Virtual Token BSC", "WOLDB") Ownable(msg.sender) {
        taxCollector = _taxCollector;
        isExcludedFromTax[msg.sender] = true;
        isExcludedFromTax[_taxCollector] = true;
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

    function pause() public onlyOwner {
        _pause();
        emit Paused(msg.sender);
    }

    function unpause() public onlyOwner {
        _unpause();
        emit Unpaused(msg.sender);
    }

    function setTaxRate(uint256 _taxRate) public onlyOwner {
        require(_taxRate <= 1000, "Tax rate too high"); // Máximo 10%
        taxRate = _taxRate;
        emit TaxUpdated(_taxRate);
    }

    function setTaxCollector(address _taxCollector) public onlyOwner {
        require(_taxCollector != address(0), "Invalid address");
        taxCollector = _taxCollector;
        isExcludedFromTax[_taxCollector] = true;
        emit TaxCollectorUpdated(_taxCollector);
    }

    function excludeFromTax(address account) public onlyOwner {
        isExcludedFromTax[account] = true;
    }

    function includeInTax(address account) public onlyOwner {
        isExcludedFromTax[account] = false;
    }

    // Funciones internas
    function _transfer(
        address sender,
        address recipient,
        uint256 amount
    ) internal override whenNotPaused {
        if (isExcludedFromTax[sender] || isExcludedFromTax[recipient]) {
            super._transfer(sender, recipient, amount);
        } else {
            uint256 taxAmount = (amount * taxRate) / 10000;
            uint256 transferAmount = amount - taxAmount;
            
            super._transfer(sender, recipient, transferAmount);
            super._transfer(sender, taxCollector, taxAmount);
        }
    }
} 