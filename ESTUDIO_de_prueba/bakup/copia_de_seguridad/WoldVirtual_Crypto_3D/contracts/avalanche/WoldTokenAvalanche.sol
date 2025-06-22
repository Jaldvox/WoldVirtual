// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";

/**
 * @title WoldTokenAvalanche
 * @dev Token del metaverso en Avalanche con gobernanza
 */
contract WoldTokenAvalanche is ERC20, ERC20Burnable, Ownable, Pausable, ERC20Votes {
    // Eventos
    event TokensMinted(address indexed to, uint256 amount);
    event TokensBurned(address indexed from, uint256 amount);
    event Paused(address account);
    event Unpaused(address account);
    event ProposalCreated(uint256 proposalId, address proposer, string description);
    event ProposalExecuted(uint256 proposalId);
    event VotingPowerUpdated(address indexed user, uint256 newPower);

    // Estructuras
    struct Proposal {
        address proposer;
        string description;
        uint256 startTime;
        uint256 endTime;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
        mapping(address => bool) hasVoted;
    }

    // Variables
    uint256 public proposalCount;
    uint256 public votingPeriod = 3 days;
    uint256 public minVotingPower = 1000 * 10**18; // 1000 tokens
    mapping(uint256 => Proposal) public proposals;
    mapping(address => uint256) public votingPower;

    // Constructor
    constructor() ERC20("Wold Virtual Token Avalanche", "WOLDA") ERC20Permit("Wold Virtual Token Avalanche") Ownable(msg.sender) {
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

    // Funciones de gobernanza
    function createProposal(string memory description) public {
        require(balanceOf(msg.sender) >= minVotingPower, "Insufficient voting power");
        
        uint256 proposalId = proposalCount++;
        Proposal storage proposal = proposals[proposalId];
        proposal.proposer = msg.sender;
        proposal.description = description;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        proposal.executed = false;

        emit ProposalCreated(proposalId, msg.sender, description);
    }

    function vote(uint256 proposalId, bool support) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp >= proposal.startTime && block.timestamp <= proposal.endTime, "Voting period ended");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(balanceOf(msg.sender) >= minVotingPower, "Insufficient voting power");

        proposal.hasVoted[msg.sender] = true;
        if (support) {
            proposal.forVotes += balanceOf(msg.sender);
        } else {
            proposal.againstVotes += balanceOf(msg.sender);
        }
    }

    function executeProposal(uint256 proposalId) public {
        Proposal storage proposal = proposals[proposalId];
        require(block.timestamp > proposal.endTime, "Voting period not ended");
        require(!proposal.executed, "Proposal already executed");
        require(proposal.forVotes > proposal.againstVotes, "Proposal not passed");

        proposal.executed = true;
        emit ProposalExecuted(proposalId);
    }

    // Funciones internas
    function _afterTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal override(ERC20, ERC20Votes) {
        super._afterTokenTransfer(from, to, amount);
        
        // Actualizar poder de voto
        if (from != address(0)) {
            votingPower[from] = balanceOf(from);
            emit VotingPowerUpdated(from, votingPower[from]);
        }
        if (to != address(0)) {
            votingPower[to] = balanceOf(to);
            emit VotingPowerUpdated(to, votingPower[to]);
        }
    }

    function _mint(address to, uint256 amount) internal override(ERC20, ERC20Votes) {
        super._mint(to, amount);
    }

    function _burn(address account, uint256 amount) internal override(ERC20, ERC20Votes) {
        super._burn(account, amount);
    }
} 