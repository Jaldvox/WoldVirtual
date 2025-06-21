// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title MetaverseNFT
 * @dev Contrato base para NFTs del metaverso
 */
contract MetaverseNFT is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    // Estructura para almacenar metadatos adicionales
    struct NFTMetadata {
        string name;
        string description;
        string category;
        uint256 creationDate;
        address creator;
        bool isTradable;
        uint256 royaltyPercentage;
    }

    // Mapeo de tokenId a metadatos
    mapping(uint256 => NFTMetadata) private _metadata;
    
    // Eventos
    event NFTMinted(uint256 indexed tokenId, address indexed creator, string uri);
    event MetadataUpdated(uint256 indexed tokenId, string uri);
    event RoyaltySet(uint256 indexed tokenId, uint256 percentage);
    event TradableStatusChanged(uint256 indexed tokenId, bool isTradable);

    constructor(string memory name, string memory symbol) 
        ERC721(name, symbol) 
        Ownable(msg.sender) 
    {}

    /**
     * @dev Función para mintear un nuevo NFT
     * @param to Dirección del propietario
     * @param uri URI de los metadatos
     * @param name Nombre del NFT
     * @param description Descripción del NFT
     * @param category Categoría del NFT
     * @param isTradable Si el NFT es comerciable
     * @param royaltyPercentage Porcentaje de royalties
     */
    function mint(
        address to,
        string memory uri,
        string memory name,
        string memory description,
        string memory category,
        bool isTradable,
        uint256 royaltyPercentage
    ) public returns (uint256) {
        require(royaltyPercentage <= 1000, "Royalty percentage too high"); // Máximo 10%
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();

        _safeMint(to, newTokenId);
        _setTokenURI(newTokenId, uri);

        _metadata[newTokenId] = NFTMetadata({
            name: name,
            description: description,
            category: category,
            creationDate: block.timestamp,
            creator: msg.sender,
            isTradable: isTradable,
            royaltyPercentage: royaltyPercentage
        });

        emit NFTMinted(newTokenId, msg.sender, uri);
        return newTokenId;
    }

    /**
     * @dev Actualiza los metadatos de un NFT
     * @param tokenId ID del token
     * @param uri Nueva URI
     */
    function updateMetadata(uint256 tokenId, string memory uri) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not owner or approved");
        _setTokenURI(tokenId, uri);
        emit MetadataUpdated(tokenId, uri);
    }

    /**
     * @dev Establece el porcentaje de royalties
     * @param tokenId ID del token
     * @param percentage Nuevo porcentaje
     */
    function setRoyalty(uint256 tokenId, uint256 percentage) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not owner or approved");
        require(percentage <= 1000, "Royalty percentage too high");
        _metadata[tokenId].royaltyPercentage = percentage;
        emit RoyaltySet(tokenId, percentage);
    }

    /**
     * @dev Cambia el estado de comerciabilidad
     * @param tokenId ID del token
     * @param isTradable Nuevo estado
     */
    function setTradable(uint256 tokenId, bool isTradable) public {
        require(_isApprovedOrOwner(msg.sender, tokenId), "Not owner or approved");
        _metadata[tokenId].isTradable = isTradable;
        emit TradableStatusChanged(tokenId, isTradable);
    }

    /**
     * @dev Obtiene los metadatos de un NFT
     * @param tokenId ID del token
     */
    function getMetadata(uint256 tokenId) public view returns (
        string memory name,
        string memory description,
        string memory category,
        uint256 creationDate,
        address creator,
        bool isTradable,
        uint256 royaltyPercentage
    ) {
        require(_exists(tokenId), "Token does not exist");
        NFTMetadata memory metadata = _metadata[tokenId];
        return (
            metadata.name,
            metadata.description,
            metadata.category,
            metadata.creationDate,
            metadata.creator,
            metadata.isTradable,
            metadata.royaltyPercentage
        );
    }

    // Funciones requeridas por las extensiones
    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 tokenId,
        uint256 batchSize
    ) internal override(ERC721, ERC721Enumerable) {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
        require(_metadata[tokenId].isTradable || from == address(0), "Token not tradable");
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage) returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721Enumerable, ERC721URIStorage) returns (bool) {
        return super.supportsInterface(interfaceId);
    }
} 