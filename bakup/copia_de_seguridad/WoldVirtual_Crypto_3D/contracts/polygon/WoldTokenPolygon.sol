// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Snapshot.sol";

/**
 * @title WoldTokenPolygon
 * @dev Token del metaverso en Polygon con características específicas
 */
contract WoldTokenPolygon is ERC20, ERC20Burnable, Ownable, Pausable, ERC20Snapshot {
    // Eventos
    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);
    event Paused(address account);
    event Unpaused(address account);
    event StakingEnabled(bool enabled);
    event StakingRewardsUpdated(uint256 newRate);
    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);

    // Variables
    bool public stakingEnabled;
    uint256 public stakingRewardRate = 1000; // 10% APY
    mapping(address => uint256) public stakedBalance;
    mapping(address => uint256) public lastStakeTime;
    mapping(address => uint256) public rewards;

    // Constructor
    constructor() ERC20("Wold Virtual Token Polygon", "WOLDP") Ownable(msg.sender) {
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

    function setStakingEnabled(bool _enabled) public onlyOwner {
        stakingEnabled = _enabled;
        emit StakingEnabled(_enabled);
    }

    function setStakingRewardRate(uint256 _rate) public onlyOwner {
        require(_rate <= 5000, "Rate too high"); // Máximo 50% APY
        stakingRewardRate = _rate;
        emit StakingRewardsUpdated(_rate);
    }

    // Funciones de staking
    function stake(uint256 amount) public whenNotPaused {
        require(stakingEnabled, "Staking disabled");
        require(amount > 0, "Amount must be > 0");
        require(balanceOf(msg.sender) >= amount, "Insufficient balance");

        // Calcular recompensas pendientes
        if (stakedBalance[msg.sender] > 0) {
            uint256 pendingRewards = calculateRewards(msg.sender);
            rewards[msg.sender] += pendingRewards;
        }

        // Actualizar staking
        _transfer(msg.sender, address(this), amount);
        stakedBalance[msg.sender] += amount;
        lastStakeTime[msg.sender] = block.timestamp;

        emit Staked(msg.sender, amount);
    }

    function unstake(uint256 amount) public whenNotPaused {
        require(amount > 0, "Amount must be > 0");
        require(stakedBalance[msg.sender] >= amount, "Insufficient staked balance");

        // Calcular y pagar recompensas
        uint256 pendingRewards = calculateRewards(msg.sender);
        rewards[msg.sender] += pendingRewards;

        // Actualizar staking
        stakedBalance[msg.sender] -= amount;
        _transfer(address(this), msg.sender, amount);

        emit Unstaked(msg.sender, amount);
    }

    function claimRewards() public whenNotPaused {
        uint256 pendingRewards = calculateRewards(msg.sender);
        require(pendingRewards > 0, "No rewards to claim");

        rewards[msg.sender] = 0;
        lastStakeTime[msg.sender] = block.timestamp;
        _mint(msg.sender, pendingRewards);

        emit RewardsClaimed(msg.sender, pendingRewards);
    }

    // Funciones internas
    function calculateRewards(address user) public view returns (uint256) {
        if (stakedBalance[user] == 0) return 0;

        uint256 timeStaked = block.timestamp - lastStakeTime[user];
        uint256 reward = (stakedBalance[user] * stakingRewardRate * timeStaked) / (365 days * 10000);
        return reward + rewards[user];
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Snapshot) whenNotPaused {
        super._beforeTokenTransfer(from, to, amount);
    }
} 