# backend/blockchain.py

class BlockchainService:
    """Servicio de ejemplo para integración blockchain/NFTs."""
    def mint_nft(self, user_address: str, metadata_uri: str) -> str:
        # Aquí iría la lógica real de minteo NFT
        return f"NFT minteado para {user_address} con metadata {metadata_uri}" 