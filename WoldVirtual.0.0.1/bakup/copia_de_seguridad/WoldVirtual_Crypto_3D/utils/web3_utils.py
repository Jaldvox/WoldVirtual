"""
Utilidades Web3 para WoldVirtual Crypto 3D
Contiene funciones para interacción con blockchain, wallets y contratos inteligentes.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Union, Any, Tuple
from decimal import Decimal
from web3 import Web3
from web3.exceptions import (
    InvalidAddress,
    ContractLogicError,
    TransactionNotFound,
    TimeExhausted,
    ValidationError
)
from eth_account import Account
from eth_account.messages import encode_defunct
import json

logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURACIÓN DE WEB3
# =============================================================================

class Web3Manager:
    """Gestor principal de Web3 para el metaverso."""
    
    def __init__(self, provider_url: str, chain_id: int = 1):
        """
        Inicializa el gestor de Web3.
        
        Args:
            provider_url: URL del proveedor Web3
            chain_id: ID de la cadena blockchain
        """
        self.provider_url = provider_url
        self.chain_id = chain_id
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = None
        self.contracts = {}
        
        # Verificar conexión
        if not self.w3.is_connected():
            raise ConnectionError(f"No se pudo conectar a {provider_url}")
        
        logger.info(f"Web3 conectado a {provider_url} (Chain ID: {chain_id})")
    
    def is_connected(self) -> bool:
        """Verifica si está conectado a la red blockchain."""
        return self.w3.is_connected()
    
    def get_network_info(self) -> Dict[str, Any]:
        """Obtiene información de la red blockchain."""
        try:
            return {
                "chain_id": self.w3.eth.chain_id,
                "block_number": self.w3.eth.block_number,
                "gas_price": self.w3.eth.gas_price,
                "is_connected": self.w3.is_connected(),
                "provider_url": self.provider_url
            }
        except Exception as e:
            logger.error(f"Error al obtener información de red: {e}")
            return {}
    
    def set_account(self, private_key: str) -> bool:
        """
        Establece la cuenta para transacciones.
        
        Args:
            private_key: Clave privada de la cuenta
            
        Returns:
            bool: True si se estableció correctamente
        """
        try:
            self.account = Account.from_key(private_key)
            logger.info(f"Cuenta establecida: {self.account.address}")
            return True
        except Exception as e:
            logger.error(f"Error al establecer cuenta: {e}")
            return False
    
    def get_account_balance(self, address: str) -> Decimal:
        """
        Obtiene el balance de una dirección.
        
        Args:
            address: Dirección de la wallet
            
        Returns:
            Decimal: Balance en ETH
        """
        try:
            balance_wei = self.w3.eth.get_balance(address)
            balance_eth = self.w3.from_wei(balance_wei, 'ether')
            return Decimal(str(balance_eth))
        except Exception as e:
            logger.error(f"Error al obtener balance: {e}")
            return Decimal('0')
    
    def estimate_gas(self, transaction: Dict[str, Any]) -> int:
        """
        Estima el gas necesario para una transacción.
        
        Args:
            transaction: Transacción a estimar
            
        Returns:
            int: Gas estimado
        """
        try:
            return self.w3.eth.estimate_gas(transaction)
        except Exception as e:
            logger.error(f"Error al estimar gas: {e}")
            return 21000  # Gas mínimo
    
    def get_gas_price(self) -> int:
        """Obtiene el precio actual del gas."""
        try:
            return self.w3.eth.gas_price
        except Exception as e:
            logger.error(f"Error al obtener precio de gas: {e}")
            return 20000000000  # 20 Gwei por defecto

# =============================================================================
# GESTIÓN DE WALLETS
# =============================================================================

class WalletManager:
    """Gestor de wallets para el metaverso."""
    
    def __init__(self, web3_manager: Web3Manager):
        """
        Inicializa el gestor de wallets.
        
        Args:
            web3_manager: Instancia del gestor Web3
        """
        self.web3_manager = web3_manager
        self.connected_wallets = {}
    
    def create_wallet(self) -> Dict[str, str]:
        """
        Crea una nueva wallet.
        
        Returns:
            Dict[str, str]: Diccionario con address y private_key
        """
        try:
            account = Account.create()
            return {
                "address": account.address,
                "private_key": account.key.hex()
            }
        except Exception as e:
            logger.error(f"Error al crear wallet: {e}")
            return {}
    
    def import_wallet_from_private_key(self, private_key: str) -> Optional[str]:
        """
        Importa una wallet desde clave privada.
        
        Args:
            private_key: Clave privada de la wallet
            
        Returns:
            Optional[str]: Dirección de la wallet o None si falla
        """
        try:
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            logger.error(f"Error al importar wallet: {e}")
            return None
    
    def validate_wallet_address(self, address: str) -> bool:
        """
        Valida una dirección de wallet.
        
        Args:
            address: Dirección a validar
            
        Returns:
            bool: True si la dirección es válida
        """
        try:
            return self.web3_manager.w3.is_address(address)
        except Exception:
            return False
    
    def get_wallet_info(self, address: str) -> Dict[str, Any]:
        """
        Obtiene información de una wallet.
        
        Args:
            address: Dirección de la wallet
            
        Returns:
            Dict[str, Any]: Información de la wallet
        """
        try:
            balance = self.web3_manager.get_account_balance(address)
            transaction_count = self.web3_manager.w3.eth.get_transaction_count(address)
            
            return {
                "address": address,
                "balance_eth": float(balance),
                "balance_wei": int(balance * (10 ** 18)),
                "transaction_count": transaction_count,
                "is_valid": self.validate_wallet_address(address)
            }
        except Exception as e:
            logger.error(f"Error al obtener información de wallet: {e}")
            return {}
    
    def sign_message(self, message: str, private_key: str) -> Optional[str]:
        """
        Firma un mensaje con una clave privada.
        
        Args:
            message: Mensaje a firmar
            private_key: Clave privada para firmar
            
        Returns:
            Optional[str]: Firma en formato hexadecimal
        """
        try:
            if private_key.startswith('0x'):
                private_key = private_key[2:]
            
            account = Account.from_key(private_key)
            message_hash = encode_defunct(text=message)
            signed_message = account.sign_message(message_hash)
            
            return signed_message.signature.hex()
        except Exception as e:
            logger.error(f"Error al firmar mensaje: {e}")
            return None
    
    def verify_signature(self, message: str, signature: str, address: str) -> bool:
        """
        Verifica la firma de un mensaje.
        
        Args:
            message: Mensaje original
            signature: Firma a verificar
            address: Dirección que debería haber firmado
            
        Returns:
            bool: True si la firma es válida
        """
        try:
            message_hash = encode_defunct(text=message)
            recovered_address = Account.recover_message(message_hash, signature=signature)
            return recovered_address.lower() == address.lower()
        except Exception as e:
            logger.error(f"Error al verificar firma: {e}")
            return False

# =============================================================================
# GESTIÓN DE TRANSACCIONES
# =============================================================================

class TransactionManager:
    """Gestor de transacciones blockchain."""
    
    def __init__(self, web3_manager: Web3Manager):
        """
        Inicializa el gestor de transacciones.
        
        Args:
            web3_manager: Instancia del gestor Web3
        """
        self.web3_manager = web3_manager
    
    def send_eth_transaction(
        self,
        to_address: str,
        amount_eth: Union[float, str],
        private_key: str,
        gas_limit: Optional[int] = None,
        gas_price: Optional[int] = None
    ) -> Optional[str]:
        """
        Envía una transacción ETH.
        
        Args:
            to_address: Dirección de destino
            amount_eth: Cantidad en ETH
            private_key: Clave privada del remitente
            gas_limit: Límite de gas (opcional)
            gas_price: Precio de gas (opcional)
            
        Returns:
            Optional[str]: Hash de la transacción o None si falla
        """
        try:
            # Preparar la transacción
            account = Account.from_key(private_key)
            nonce = self.web3_manager.w3.eth.get_transaction_count(account.address)
            
            # Convertir ETH a Wei
            amount_wei = self.web3_manager.w3.to_wei(amount_eth, 'ether')
            
            # Configurar gas
            if gas_price is None:
                gas_price = self.web3_manager.get_gas_price()
            
            if gas_limit is None:
                gas_limit = self.web3_manager.estimate_gas({
                    'to': to_address,
                    'value': amount_wei,
                    'from': account.address
                })
            
            # Crear transacción
            transaction = {
                'nonce': nonce,
                'to': to_address,
                'value': amount_wei,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'chainId': self.web3_manager.chain_id
            }
            
            # Firmar y enviar transacción
            signed_txn = self.web3_manager.w3.eth.account.sign_transaction(
                transaction, private_key
            )
            tx_hash = self.web3_manager.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )
            
            logger.info(f"Transacción enviada: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"Error al enviar transacción: {e}")
            return None
    
    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el recibo de una transacción.
        
        Args:
            tx_hash: Hash de la transacción
            
        Returns:
            Optional[Dict[str, Any]]: Recibo de la transacción
        """
        try:
            receipt = self.web3_manager.w3.eth.get_transaction_receipt(tx_hash)
            if receipt:
                return {
                    "transaction_hash": receipt['transactionHash'].hex(),
                    "block_number": receipt['blockNumber'],
                    "gas_used": receipt['gasUsed'],
                    "status": receipt['status'],
                    "effective_gas_price": receipt['effectiveGasPrice'],
                    "cumulative_gas_used": receipt['cumulativeGasUsed']
                }
            return None
        except Exception as e:
            logger.error(f"Error al obtener recibo de transacción: {e}")
            return None
    
    def wait_for_transaction(self, tx_hash: str, timeout: int = 300) -> Optional[Dict[str, Any]]:
        """
        Espera a que una transacción sea confirmada.
        
        Args:
            tx_hash: Hash de la transacción
            timeout: Tiempo máximo de espera en segundos
            
        Returns:
            Optional[Dict[str, Any]]: Recibo de la transacción confirmada
        """
        try:
            receipt = self.web3_manager.w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=timeout
            )
            return self.get_transaction_receipt(tx_hash)
        except TimeExhausted:
            logger.error(f"Tiempo de espera agotado para transacción: {tx_hash}")
            return None
        except Exception as e:
            logger.error(f"Error al esperar transacción: {e}")
            return None
    
    def get_transaction_status(self, tx_hash: str) -> str:
        """
        Obtiene el estado de una transacción.
        
        Args:
            tx_hash: Hash de la transacción
            
        Returns:
            str: Estado de la transacción
        """
        try:
            receipt = self.get_transaction_receipt(tx_hash)
            if receipt:
                return "confirmed" if receipt['status'] == 1 else "failed"
            else:
                # Verificar si la transacción existe
                try:
                    tx = self.web3_manager.w3.eth.get_transaction(tx_hash)
                    return "pending" if tx else "not_found"
                except TransactionNotFound:
                    return "not_found"
        except Exception as e:
            logger.error(f"Error al obtener estado de transacción: {e}")
            return "error"

# =============================================================================
# GESTIÓN DE CONTRATOS INTELIGENTES
# =============================================================================

class SmartContractManager:
    """Gestor de contratos inteligentes."""
    
    def __init__(self, web3_manager: Web3Manager):
        """
        Inicializa el gestor de contratos.
        
        Args:
            web3_manager: Instancia del gestor Web3
        """
        self.web3_manager = web3_manager
        self.contracts = {}
    
    def load_contract(self, contract_address: str, abi: List[Dict]) -> bool:
        """
        Carga un contrato inteligente.
        
        Args:
            contract_address: Dirección del contrato
            abi: ABI del contrato
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            contract = self.web3_manager.w3.eth.contract(
                address=contract_address, abi=abi
            )
            self.contracts[contract_address] = contract
            logger.info(f"Contrato cargado: {contract_address}")
            return True
        except Exception as e:
            logger.error(f"Error al cargar contrato: {e}")
            return False
    
    def call_contract_function(
        self,
        contract_address: str,
        function_name: str,
        *args,
        **kwargs
    ) -> Any:
        """
        Llama a una función de solo lectura de un contrato.
        
        Args:
            contract_address: Dirección del contrato
            function_name: Nombre de la función
            *args: Argumentos de la función
            **kwargs: Argumentos nombrados
            
        Returns:
            Any: Resultado de la función
        """
        try:
            if contract_address not in self.contracts:
                raise ValueError(f"Contrato no cargado: {contract_address}")
            
            contract = self.contracts[contract_address]
            function = getattr(contract.functions, function_name)
            result = function(*args, **kwargs).call()
            
            return result
        except Exception as e:
            logger.error(f"Error al llamar función de contrato: {e}")
            return None
    
    def send_contract_transaction(
        self,
        contract_address: str,
        function_name: str,
        private_key: str,
        *args,
        gas_limit: Optional[int] = None,
        gas_price: Optional[int] = None,
        **kwargs
    ) -> Optional[str]:
        """
        Envía una transacción a un contrato inteligente.
        
        Args:
            contract_address: Dirección del contrato
            function_name: Nombre de la función
            private_key: Clave privada para firmar
            *args: Argumentos de la función
            gas_limit: Límite de gas (opcional)
            gas_price: Precio de gas (opcional)
            **kwargs: Argumentos nombrados
            
        Returns:
            Optional[str]: Hash de la transacción
        """
        try:
            if contract_address not in self.contracts:
                raise ValueError(f"Contrato no cargado: {contract_address}")
            
            contract = self.contracts[contract_address]
            account = Account.from_key(private_key)
            
            # Obtener función
            function = getattr(contract.functions, function_name)
            
            # Construir transacción
            transaction = function(*args, **kwargs).build_transaction({
                'from': account.address,
                'nonce': self.web3_manager.w3.eth.get_transaction_count(account.address),
                'gas': gas_limit or 200000,
                'gasPrice': gas_price or self.web3_manager.get_gas_price()
            })
            
            # Firmar y enviar
            signed_txn = self.web3_manager.w3.eth.account.sign_transaction(
                transaction, private_key
            )
            tx_hash = self.web3_manager.w3.eth.send_raw_transaction(
                signed_txn.rawTransaction
            )
            
            logger.info(f"Transacción de contrato enviada: {tx_hash.hex()}")
            return tx_hash.hex()
            
        except Exception as e:
            logger.error(f"Error al enviar transacción de contrato: {e}")
            return None
    
    def get_contract_events(
        self,
        contract_address: str,
        event_name: str,
        from_block: int = 0,
        to_block: str = "latest"
    ) -> List[Dict[str, Any]]:
        """
        Obtiene eventos de un contrato.
        
        Args:
            contract_address: Dirección del contrato
            event_name: Nombre del evento
            from_block: Bloque inicial
            to_block: Bloque final
            
        Returns:
            List[Dict[str, Any]]: Lista de eventos
        """
        try:
            if contract_address not in self.contracts:
                raise ValueError(f"Contrato no cargado: {contract_address}")
            
            contract = self.contracts[contract_address]
            event = getattr(contract.events, event_name)
            events = event.get_logs(fromBlock=from_block, toBlock=to_block)
            
            return [
                {
                    "transaction_hash": event['transactionHash'].hex(),
                    "block_number": event['blockNumber'],
                    "log_index": event['logIndex'],
                    "args": event['args']
                }
                for event in events
            ]
        except Exception as e:
            logger.error(f"Error al obtener eventos del contrato: {e}")
            return []

# =============================================================================
# UTILIDADES DE TOKENS
# =============================================================================

class TokenUtils:
    """Utilidades para manejo de tokens."""
    
    @staticmethod
    def format_token_amount(amount: Union[int, str], decimals: int = 18) -> str:
        """
        Formatea una cantidad de tokens.
        
        Args:
            amount: Cantidad en unidades más pequeñas
            decimals: Número de decimales del token
            
        Returns:
            str: Cantidad formateada
        """
        try:
            if isinstance(amount, str):
                amount = int(amount)
            
            # Convertir a decimal para precisión
            decimal_amount = Decimal(str(amount)) / Decimal(str(10 ** decimals))
            
            # Formatear según el tamaño
            if decimal_amount >= 1:
                return f"{decimal_amount:.4f}"
            elif decimal_amount >= 0.0001:
                return f"{decimal_amount:.6f}"
            else:
                return f"{decimal_amount:.8f}"
        except Exception as e:
            logger.error(f"Error al formatear cantidad de token: {e}")
            return "0.0000"
    
    @staticmethod
    def parse_token_amount(amount: str, decimals: int = 18) -> int:
        """
        Parsea una cantidad de tokens a unidades más pequeñas.
        
        Args:
            amount: Cantidad formateada
            decimals: Número de decimales del token
            
        Returns:
            int: Cantidad en unidades más pequeñas
        """
        try:
            decimal_amount = Decimal(amount)
            return int(decimal_amount * Decimal(str(10 ** decimals)))
        except Exception as e:
            logger.error(f"Error al parsear cantidad de token: {e}")
            return 0
    
    @staticmethod
    def calculate_token_percentage(amount: int, total: int, decimals: int = 18) -> float:
        """
        Calcula el porcentaje de tokens.
        
        Args:
            amount: Cantidad de tokens
            total: Total de tokens
            decimals: Número de decimales del token
            
        Returns:
            float: Porcentaje
        """
        try:
            if total == 0:
                return 0.0
            
            percentage = (amount / total) * 100
            return round(percentage, 2)
        except Exception as e:
            logger.error(f"Error al calcular porcentaje de tokens: {e}")
            return 0.0

# =============================================================================
# FUNCIONES DE UTILIDAD GENERAL
# =============================================================================

def get_network_name(chain_id: int) -> str:
    """
    Obtiene el nombre de la red basado en el chain ID.
    
    Args:
        chain_id: ID de la cadena
        
    Returns:
        str: Nombre de la red
    """
    networks = {
        1: "Ethereum Mainnet",
        3: "Ropsten Testnet",
        4: "Rinkeby Testnet",
        5: "Goerli Testnet",
        42: "Kovan Testnet",
        56: "BSC Mainnet",
        97: "BSC Testnet",
        137: "Polygon Mainnet",
        80001: "Polygon Mumbai Testnet",
        42161: "Arbitrum One",
        10: "Optimism"
    }
    
    return networks.get(chain_id, f"Unknown Network (Chain ID: {chain_id})")

def is_testnet(chain_id: int) -> bool:
    """
    Verifica si una red es testnet.
    
    Args:
        chain_id: ID de la cadena
        
    Returns:
        bool: True si es testnet
    """
    testnet_ids = [3, 4, 5, 42, 97, 80001]
    return chain_id in testnet_ids

def get_explorer_url(chain_id: int, tx_hash: str) -> str:
    """
    Obtiene la URL del explorador de bloques para una transacción.
    
    Args:
        chain_id: ID de la cadena
        tx_hash: Hash de la transacción
        
    Returns:
        str: URL del explorador
    """
    explorers = {
        1: f"https://etherscan.io/tx/{tx_hash}",
        3: f"https://ropsten.etherscan.io/tx/{tx_hash}",
        4: f"https://rinkeby.etherscan.io/tx/{tx_hash}",
        5: f"https://goerli.etherscan.io/tx/{tx_hash}",
        42: f"https://kovan.etherscan.io/tx/{tx_hash}",
        56: f"https://bscscan.com/tx/{tx_hash}",
        97: f"https://testnet.bscscan.com/tx/{tx_hash}",
        137: f"https://polygonscan.com/tx/{tx_hash}",
        80001: f"https://mumbai.polygonscan.com/tx/{tx_hash}",
        42161: f"https://arbiscan.io/tx/{tx_hash}",
        10: f"https://optimistic.etherscan.io/tx/{tx_hash}"
    }
    
    return explorers.get(chain_id, f"Unknown explorer for chain {chain_id}")

def validate_transaction_hash(tx_hash: str) -> bool:
    """
    Valida el formato de un hash de transacción.
    
    Args:
        tx_hash: Hash de la transacción
        
    Returns:
        bool: True si el formato es válido
    """
    if not tx_hash:
        return False
    
    # Verificar formato hexadecimal de 64 caracteres (32 bytes)
    pattern = r'^0x[a-fA-F0-9]{64}$'
    return bool(re.match(pattern, tx_hash)) 