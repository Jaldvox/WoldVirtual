# Contratos Inteligentes del Metaverso

## Descripción
Esta carpeta contiene los contratos inteligentes que gestionan la lógica de negocio en la blockchain, incluyendo NFTs, tokens y gobernanza del metaverso.

## Estructura de Carpetas
- `nft/`: Contratos para NFTs (avatares, terrenos, items)
- `token/`: Contratos de tokens fungibles
- `marketplace/`: Contratos para el marketplace
- `governance/`: Contratos de gobernanza
- `tests/`: Tests de contratos
- `scripts/`: Scripts de despliegue y mantenimiento

## Tecnologías Principales
- Solidity
- Hardhat/Truffle
- Web3.js
- OpenZeppelin

## Contratos Principales

### 1. MetaverseNFT (`nft/MetaverseNFT.sol`)
Contrato base para NFTs del metaverso.

#### Características:
- Implementación ERC-721
- Metadata on-chain y off-chain
- Sistema de royalties
- Gestión de permisos
- Eventos personalizados

### 2. LandRegistry (`nft/LandRegistry.sol`)
Registro de terrenos virtuales.

#### Características:
- Mapeo de coordenadas a propietarios
- Sistema de parcelas
- Restricciones de construcción
- Gestión de recursos
- Eventos de transferencia

### 3. AvatarNFT (`nft/AvatarNFT.sol`)
NFTs de avatares personalizables.

#### Características:
- Atributos personalizables
- Sistema de niveles
- Experiencia y habilidades
- Inventario integrado
- Eventos de progreso

### 4. ItemNFT (`nft/ItemNFT.sol`)
NFTs de items y objetos.

#### Características:
- Implementación ERC-1155
- Atributos y estadísticas
- Durabilidad y uso
- Combinación y mejora
- Eventos de uso

### 5. Marketplace (`marketplace/Marketplace.sol`)
Marketplace descentralizado.

#### Características:
- Listado de NFTs
- Subastas y ventas directas
- Sistema de ofertas
- Gestión de royalties
- Eventos de transacción

### 6. GovernanceToken (`governance/GovernanceToken.sol`)
Token de gobernanza del metaverso.

#### Características:
- Implementación ERC-20
- Staking y recompensas
- Votación y propuestas
- Delegación de votos
- Eventos de gobernanza

## Desarrollo

### Requisitos
- Node.js 16+
- npm 7+
- Solidity 0.8.0+
- Hardhat/Truffle

### Instalación
```bash
# Instalar dependencias
npm install

# Instalar plugins de Hardhat
npm install --save-dev @nomiclabs/hardhat-ethers ethers @nomiclabs/hardhat-waffle ethereum-waffle chai @nomiclabs/hardhat-etherscan
```

### Compilación
```bash
# Compilar contratos
npx hardhat compile

# Verificar contratos
npx hardhat verify --network <network> <contract_address>
```

### Testing
```bash
# Ejecutar tests
npx hardhat test

# Ejecutar tests con cobertura
npx hardhat coverage
```

### Despliegue
```bash
# Desplegar en red local
npx hardhat node
npx hardhat run scripts/deploy.js --network localhost

# Desplegar en testnet
npx hardhat run scripts/deploy.js --network <testnet>
```

## Seguridad

### Auditorías
- Auditorías externas
- Tests de penetración
- Análisis estático
- Revisión de código

### Mejores Prácticas
- Patrones de seguridad probados
- Manejo seguro de fondos
- Control de acceso
- Eventos y logs
- Manejo de errores

### Integración con OpenZeppelin
- Contratos base seguros
- Implementaciones estándar
- Actualizaciones de seguridad
- Documentación detallada

## Convenciones de Código

### Estilo
- Seguir estándares de Solidity
- Documentación NatSpec
- Nombres descriptivos
- Comentarios claros

### Optimización
- Optimización de gas
- Patrones de diseño eficientes
- Reutilización de código
- Testing exhaustivo

### Eventos
- Eventos para acciones importantes
- Parámetros indexados
- Documentación clara
- Manejo de logs

## Mantenimiento

### Monitoreo
- Monitoreo de eventos
- Alertas de seguridad
- Métricas de uso
- Logs de transacciones

### Actualizaciones
- Versiones de contratos
- Migraciones de datos
- Actualizaciones de seguridad
- Mejoras de rendimiento

## Contribución
1. Fork del repositorio
2. Crear rama de feature
3. Commit de cambios
4. Push a la rama
5. Crear Pull Request

## Licencia
Este proyecto está bajo la Licencia MIT. 