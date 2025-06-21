// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "./MetaverseNFT.sol";

/**
 * @title LandRegistry
 * @dev Contrato para el registro de terrenos virtuales
 */
contract LandRegistry is Ownable, ReentrancyGuard {
    MetaverseNFT public landNFT;

    // Estructura para coordenadas
    struct Coordinates {
        int256 x;
        int256 y;
        int256 z;
    }

    // Estructura para parcelas
    struct Parcel {
        uint256 tokenId;
        address owner;
        Coordinates coordinates;
        uint256 size;
        bool isBuildable;
        uint256 lastModified;
        string metadata;
    }

    // Mapeo de coordenadas a tokenId
    mapping(int256 => mapping(int256 => mapping(int256 => uint256))) public coordinateToTokenId;
    
    // Mapeo de tokenId a parcela
    mapping(uint256 => Parcel) public parcels;

    // Eventos
    event ParcelRegistered(uint256 indexed tokenId, address indexed owner, Coordinates coordinates);
    event ParcelUpdated(uint256 indexed tokenId, string metadata);
    event BuildableStatusChanged(uint256 indexed tokenId, bool isBuildable);
    event ParcelTransferred(uint256 indexed tokenId, address indexed from, address indexed to);

    constructor(address _landNFT) Ownable(msg.sender) {
        landNFT = MetaverseNFT(_landNFT);
    }

    /**
     * @dev Registra una nueva parcela
     * @param coordinates Coordenadas de la parcela
     * @param size Tamaño de la parcela
     * @param metadata Metadatos de la parcela
     */
    function registerParcel(
        Coordinates memory coordinates,
        uint256 size,
        string memory metadata
    ) public nonReentrant returns (uint256) {
        require(
            coordinateToTokenId[coordinates.x][coordinates.y][coordinates.z] == 0,
            "Coordinates already registered"
        );

        // Mintear NFT de terreno
        uint256 tokenId = landNFT.mint(
            msg.sender,
            metadata,
            "Virtual Land",
            "A piece of virtual land in the metaverse",
            "land",
            true,
            250 // 2.5% royalty
        );

        // Registrar parcela
        parcels[tokenId] = Parcel({
            tokenId: tokenId,
            owner: msg.sender,
            coordinates: coordinates,
            size: size,
            isBuildable: true,
            lastModified: block.timestamp,
            metadata: metadata
        });

        coordinateToTokenId[coordinates.x][coordinates.y][coordinates.z] = tokenId;

        emit ParcelRegistered(tokenId, msg.sender, coordinates);
        return tokenId;
    }

    /**
     * @dev Actualiza los metadatos de una parcela
     * @param tokenId ID del token
     * @param metadata Nuevos metadatos
     */
    function updateParcelMetadata(uint256 tokenId, string memory metadata) public {
        require(parcels[tokenId].owner == msg.sender, "Not parcel owner");
        parcels[tokenId].metadata = metadata;
        parcels[tokenId].lastModified = block.timestamp;
        emit ParcelUpdated(tokenId, metadata);
    }

    /**
     * @dev Cambia el estado de construcción de una parcela
     * @param tokenId ID del token
     * @param isBuildable Nuevo estado
     */
    function setBuildable(uint256 tokenId, bool isBuildable) public {
        require(parcels[tokenId].owner == msg.sender, "Not parcel owner");
        parcels[tokenId].isBuildable = isBuildable;
        emit BuildableStatusChanged(tokenId, isBuildable);
    }

    /**
     * @dev Obtiene información de una parcela
     * @param tokenId ID del token
     */
    function getParcelInfo(uint256 tokenId) public view returns (
        address owner,
        Coordinates memory coordinates,
        uint256 size,
        bool isBuildable,
        uint256 lastModified,
        string memory metadata
    ) {
        Parcel memory parcel = parcels[tokenId];
        return (
            parcel.owner,
            parcel.coordinates,
            parcel.size,
            parcel.isBuildable,
            parcel.lastModified,
            parcel.metadata
        );
    }

    /**
     * @dev Verifica si una parcela está disponible
     * @param coordinates Coordenadas a verificar
     */
    function isParcelAvailable(Coordinates memory coordinates) public view returns (bool) {
        return coordinateToTokenId[coordinates.x][coordinates.y][coordinates.z] == 0;
    }

    /**
     * @dev Obtiene el tokenId de una parcela por coordenadas
     * @param coordinates Coordenadas de la parcela
     */
    function getTokenIdByCoordinates(Coordinates memory coordinates) public view returns (uint256) {
        return coordinateToTokenId[coordinates.x][coordinates.y][coordinates.z];
    }

    /**
     * @dev Hook para manejar transferencias de NFT
     * @param from Dirección del remitente
     * @param to Dirección del destinatario
     * @param tokenId ID del token
     */
    function onTransfer(address from, address to, uint256 tokenId) external {
        require(msg.sender == address(landNFT), "Only land NFT can call");
        parcels[tokenId].owner = to;
        emit ParcelTransferred(tokenId, from, to);
    }
} 