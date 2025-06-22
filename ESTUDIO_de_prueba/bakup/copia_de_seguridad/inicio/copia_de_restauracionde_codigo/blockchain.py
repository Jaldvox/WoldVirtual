import os
from typing import Optional
# from web3 import Web3
# import json

# Configuración desde variables de entorno o archivo
WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
NFT_CONTRACT_ADDRESS = os.getenv("NFT_CONTRACT_ADDRESS", "0x0000000000000000000000000000000000000000")
NFT_CONTRACT_ABI_PATH = os.getenv("NFT_CONTRACT_ABI_PATH", "contracts/nft/MetaverseNFT.abi.json")

class BlockchainService:
    """
    Servicio para integración blockchain/NFTs usando Web3.py.

    NOTA: Este código está preparado pero NO está conectado ni activo en la lógica principal.
    Para activarlo, asegúrate de tener:
      - Un nodo Ethereum o proveedor (Infura, Alchemy, etc.)
      - El ABI del contrato NFT en la ruta especificada
      - Claves privadas seguras y nunca expuestas en frontend
    """
    def __init__(self):
        # self.w3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER_URL))
        # with open(NFT_CONTRACT_ABI_PATH, 'r') as f:
        #     abi = json.load(f)
        # self.nft_contract = self.w3.eth.contract(address=NFT_CONTRACT_ADDRESS, abi=abi)
        pass

    def mint_nft(self, user_address: str, metadata_uri: str, private_key: str) -> Optional[str]:
        """
        Mintea un NFT usando el contrato MetaverseNFT.
        Parámetros:
          - user_address: dirección Ethereum del usuario que recibirá el NFT
          - metadata_uri: URI de los metadatos (ej. JSON en IPFS)
          - private_key: clave privada del minteador (NO exponer nunca en frontend)
        Devuelve:
          - Hash de la transacción si es exitoso, None si falla.
        Dependencias:
          - web3.py instalado y configurado
          - ABI del contrato NFT
        Para activar:
          - Descomentar el código y asegurar la configuración correcta
        """
        # try:
        #     nonce = self.w3.eth.get_transaction_count(user_address)
        #     txn = self.nft_contract.functions.mint(
        #         user_address,
        #         metadata_uri,
        #         "Asset NFT",
        #         "NFT del metaverso",
        #         "asset",
        #         True,
        #         250 # 2.5% royalty
        #     ).build_transaction({
        #         'from': user_address,
        #         'nonce': nonce,
        #         'gas': 300000,
        #         'gasPrice': self.w3.to_wei('20', 'gwei')
        #     })
        #     signed_txn = self.w3.eth.account.sign_transaction(txn, private_key=private_key)
        #     tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        #     return self.w3.to_hex(tx_hash)
        # except Exception as e:
        #     print(f"Error minteando NFT: {e}")
        #     return None
        return None  # Placeholder

    def get_nft_owner(self, token_id: int) -> Optional[str]:
        """
        Consulta el propietario de un NFT.
        Parámetros:
          - token_id: ID del token NFT
        Devuelve:
          - Dirección Ethereum del propietario, o None si falla.
        Dependencias:
          - web3.py instalado y configurado
        """
        # try:
        #     return self.nft_contract.functions.ownerOf(token_id).call()
        # except Exception as e:
        #     print(f"Error consultando propietario NFT: {e}")
        #     return None
        return None  # Placeholder

    def get_nft_metadata(self, token_id: int) -> Optional[str]:
        """
        Consulta la URI de metadatos de un NFT.
        Parámetros:
          - token_id: ID del token NFT
        Devuelve:
          - URI de metadatos (ej. JSON en IPFS), o None si falla.
        Dependencias:
          - web3.py instalado y configurado
        """
        # try:
        #     return self.nft_contract.functions.tokenURI(token_id).call()
        # except Exception as e:
        #     print(f"Error consultando metadata NFT: {e}")
        #     return None
        return None  # Placeholder 