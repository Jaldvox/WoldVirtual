// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title Marketplace
 * @dev Contrato para el marketplace de NFTs
 */
contract Marketplace is ReentrancyGuard, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _listingIds;

    // Estructura para listados
    struct Listing {
        uint256 listingId;
        address nftContract;
        uint256 tokenId;
        address seller;
        address paymentToken;
        uint256 price;
        bool isActive;
        uint256 createdAt;
        uint256 expiresAt;
    }

    // Estructura para ofertas
    struct Offer {
        address bidder;
        uint256 amount;
        uint256 timestamp;
        bool isActive;
    }

    // Mapeo de listingId a Listing
    mapping(uint256 => Listing) public listings;
    
    // Mapeo de tokenId a listingId
    mapping(address => mapping(uint256 => uint256)) public tokenToListingId;
    
    // Mapeo de listingId a ofertas
    mapping(uint256 => Offer[]) public listingOffers;

    // Fee del marketplace (en basis points, 1% = 100)
    uint256 public marketplaceFee = 250; // 2.5%
    
    // Dirección del fee collector
    address public feeCollector;

    // Eventos
    event ListingCreated(
        uint256 indexed listingId,
        address indexed nftContract,
        uint256 indexed tokenId,
        address seller,
        uint256 price
    );
    event ListingUpdated(uint256 indexed listingId, uint256 newPrice);
    event ListingCancelled(uint256 indexed listingId);
    event ItemSold(
        uint256 indexed listingId,
        address indexed nftContract,
        uint256 indexed tokenId,
        address seller,
        address buyer,
        uint256 price
    );
    event OfferMade(
        uint256 indexed listingId,
        address indexed bidder,
        uint256 amount
    );
    event OfferAccepted(
        uint256 indexed listingId,
        address indexed bidder,
        uint256 amount
    );
    event OfferCancelled(uint256 indexed listingId, address indexed bidder);

    constructor(address _feeCollector) Ownable(msg.sender) {
        feeCollector = _feeCollector;
    }

    /**
     * @dev Crea un nuevo listado
     * @param nftContract Dirección del contrato NFT
     * @param tokenId ID del token
     * @param paymentToken Dirección del token de pago
     * @param price Precio
     * @param duration Duración del listado en segundos
     */
    function createListing(
        address nftContract,
        uint256 tokenId,
        address paymentToken,
        uint256 price,
        uint256 duration
    ) external nonReentrant returns (uint256) {
        require(price > 0, "Price must be greater than 0");
        require(duration > 0, "Duration must be greater than 0");
        
        // Verificar que el vendedor es el propietario
        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        _listingIds.increment();
        uint256 listingId = _listingIds.current();

        listings[listingId] = Listing({
            listingId: listingId,
            nftContract: nftContract,
            tokenId: tokenId,
            seller: msg.sender,
            paymentToken: paymentToken,
            price: price,
            isActive: true,
            createdAt: block.timestamp,
            expiresAt: block.timestamp + duration
        });

        tokenToListingId[nftContract][tokenId] = listingId;

        emit ListingCreated(listingId, nftContract, tokenId, msg.sender, price);
        return listingId;
    }

    /**
     * @dev Actualiza el precio de un listado
     * @param listingId ID del listado
     * @param newPrice Nuevo precio
     */
    function updateListingPrice(uint256 listingId, uint256 newPrice) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not the seller");
        require(listing.isActive, "Listing not active");
        require(newPrice > 0, "Price must be greater than 0");

        listing.price = newPrice;
        emit ListingUpdated(listingId, newPrice);
    }

    /**
     * @dev Cancela un listado
     * @param listingId ID del listado
     */
    function cancelListing(uint256 listingId) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not the seller");
        require(listing.isActive, "Listing not active");

        listing.isActive = false;
        IERC721(listing.nftContract).transferFrom(
            address(this),
            msg.sender,
            listing.tokenId
        );

        emit ListingCancelled(listingId);
    }

    /**
     * @dev Compra un NFT listado
     * @param listingId ID del listado
     */
    function buyItem(uint256 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.isActive, "Listing not active");
        require(block.timestamp <= listing.expiresAt, "Listing expired");
        require(msg.sender != listing.seller, "Cannot buy your own item");

        uint256 price = listing.price;
        if (listing.paymentToken == address(0)) {
            require(msg.value >= price, "Insufficient payment");
        } else {
            IERC20(listing.paymentToken).transferFrom(
                msg.sender,
                address(this),
                price
            );
        }

        // Calcular y transferir fees
        uint256 feeAmount = (price * marketplaceFee) / 10000;
        uint256 sellerAmount = price - feeAmount;

        if (listing.paymentToken == address(0)) {
            payable(feeCollector).transfer(feeAmount);
            payable(listing.seller).transfer(sellerAmount);
        } else {
            IERC20(listing.paymentToken).transfer(feeCollector, feeAmount);
            IERC20(listing.paymentToken).transfer(listing.seller, sellerAmount);
        }

        // Transferir NFT al comprador
        IERC721(listing.nftContract).transferFrom(
            address(this),
            msg.sender,
            listing.tokenId
        );

        listing.isActive = false;

        emit ItemSold(
            listingId,
            listing.nftContract,
            listing.tokenId,
            listing.seller,
            msg.sender,
            price
        );
    }

    /**
     * @dev Hace una oferta por un NFT
     * @param listingId ID del listado
     * @param amount Cantidad ofrecida
     */
    function makeOffer(uint256 listingId, uint256 amount) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.isActive, "Listing not active");
        require(block.timestamp <= listing.expiresAt, "Listing expired");
        require(msg.sender != listing.seller, "Cannot offer on your own item");

        if (listing.paymentToken == address(0)) {
            require(msg.value >= amount, "Insufficient payment");
        } else {
            IERC20(listing.paymentToken).transferFrom(
                msg.sender,
                address(this),
                amount
            );
        }

        listingOffers[listingId].push(Offer({
            bidder: msg.sender,
            amount: amount,
            timestamp: block.timestamp,
            isActive: true
        }));

        emit OfferMade(listingId, msg.sender, amount);
    }

    /**
     * @dev Acepta una oferta
     * @param listingId ID del listado
     * @param offerIndex Índice de la oferta
     */
    function acceptOffer(uint256 listingId, uint256 offerIndex) external nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not the seller");
        require(listing.isActive, "Listing not active");

        Offer storage offer = listingOffers[listingId][offerIndex];
        require(offer.isActive, "Offer not active");

        uint256 amount = offer.amount;
        offer.isActive = false;

        // Calcular y transferir fees
        uint256 feeAmount = (amount * marketplaceFee) / 10000;
        uint256 sellerAmount = amount - feeAmount;

        if (listing.paymentToken == address(0)) {
            payable(feeCollector).transfer(feeAmount);
            payable(listing.seller).transfer(sellerAmount);
        } else {
            IERC20(listing.paymentToken).transfer(feeCollector, feeAmount);
            IERC20(listing.paymentToken).transfer(listing.seller, sellerAmount);
        }

        // Transferir NFT al comprador
        IERC721(listing.nftContract).transferFrom(
            address(this),
            offer.bidder,
            listing.tokenId
        );

        listing.isActive = false;

        emit OfferAccepted(listingId, offer.bidder, amount);
    }

    /**
     * @dev Cancela una oferta
     * @param listingId ID del listado
     * @param offerIndex Índice de la oferta
     */
    function cancelOffer(uint256 listingId, uint256 offerIndex) external nonReentrant {
        Offer storage offer = listingOffers[listingId][offerIndex];
        require(offer.bidder == msg.sender, "Not the bidder");
        require(offer.isActive, "Offer not active");

        offer.isActive = false;

        Listing storage listing = listings[listingId];
        if (listing.paymentToken == address(0)) {
            payable(msg.sender).transfer(offer.amount);
        } else {
            IERC20(listing.paymentToken).transfer(msg.sender, offer.amount);
        }

        emit OfferCancelled(listingId, msg.sender);
    }

    /**
     * @dev Obtiene las ofertas activas de un listado
     * @param listingId ID del listado
     */
    function getActiveOffers(uint256 listingId) external view returns (Offer[] memory) {
        Offer[] storage allOffers = listingOffers[listingId];
        uint256 activeCount = 0;
        
        for (uint256 i = 0; i < allOffers.length; i++) {
            if (allOffers[i].isActive) {
                activeCount++;
            }
        }

        Offer[] memory activeOffers = new Offer[](activeCount);
        uint256 currentIndex = 0;
        
        for (uint256 i = 0; i < allOffers.length; i++) {
            if (allOffers[i].isActive) {
                activeOffers[currentIndex] = allOffers[i];
                currentIndex++;
            }
        }

        return activeOffers;
    }

    /**
     * @dev Actualiza el fee del marketplace
     * @param newFee Nuevo fee en basis points
     */
    function updateMarketplaceFee(uint256 newFee) external onlyOwner {
        require(newFee <= 1000, "Fee too high"); // Máximo 10%
        marketplaceFee = newFee;
    }

    /**
     * @dev Actualiza el fee collector
     * @param newFeeCollector Nueva dirección del fee collector
     */
    function updateFeeCollector(address newFeeCollector) external onlyOwner {
        require(newFeeCollector != address(0), "Invalid address");
        feeCollector = newFeeCollector;
    }
} 