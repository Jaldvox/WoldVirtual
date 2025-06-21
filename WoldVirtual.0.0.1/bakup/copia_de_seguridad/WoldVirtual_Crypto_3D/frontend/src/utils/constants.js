export const SUPPORTED_CHAINS = {
  MAINNET: 1,
  ROPSTEN: 3,
  RINKEBY: 4,
  GOERLI: 5,
  KOVAN: 42,
  BSC: 56,
  BSC_TESTNET: 97,
  POLYGON: 137,
  MUMBAI: 80001,
};

export const CHAIN_NAMES = {
  [SUPPORTED_CHAINS.MAINNET]: 'Ethereum Mainnet',
  [SUPPORTED_CHAINS.ROPSTEN]: 'Ropsten Testnet',
  [SUPPORTED_CHAINS.RINKEBY]: 'Rinkeby Testnet',
  [SUPPORTED_CHAINS.GOERLI]: 'Goerli Testnet',
  [SUPPORTED_CHAINS.KOVAN]: 'Kovan Testnet',
  [SUPPORTED_CHAINS.BSC]: 'BSC Mainnet',
  [SUPPORTED_CHAINS.BSC_TESTNET]: 'BSC Testnet',
  [SUPPORTED_CHAINS.POLYGON]: 'Polygon Mainnet',
  [SUPPORTED_CHAINS.MUMBAI]: 'Mumbai Testnet',
};

export const CHAIN_CURRENCIES = {
  [SUPPORTED_CHAINS.MAINNET]: 'ETH',
  [SUPPORTED_CHAINS.ROPSTEN]: 'ETH',
  [SUPPORTED_CHAINS.RINKEBY]: 'ETH',
  [SUPPORTED_CHAINS.GOERLI]: 'ETH',
  [SUPPORTED_CHAINS.KOVAN]: 'ETH',
  [SUPPORTED_CHAINS.BSC]: 'BNB',
  [SUPPORTED_CHAINS.BSC_TESTNET]: 'BNB',
  [SUPPORTED_CHAINS.POLYGON]: 'MATIC',
  [SUPPORTED_CHAINS.MUMBAI]: 'MATIC',
};

export const ASSET_CATEGORIES = {
  BUILDINGS: 'buildings',
  NATURE: 'nature',
  CHARACTERS: 'characters',
  EFFECTS: 'effects',
};

export const ASSET_CATEGORY_NAMES = {
  [ASSET_CATEGORIES.BUILDINGS]: 'Edificios',
  [ASSET_CATEGORIES.NATURE]: 'Naturaleza',
  [ASSET_CATEGORIES.CHARACTERS]: 'Personajes',
  [ASSET_CATEGORIES.EFFECTS]: 'Efectos',
};

export const FILE_TYPES = {
  IMAGE: ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
  MODEL: ['model/gltf-binary', 'model/gltf+json'],
};

export const MAX_FILE_SIZES = {
  IMAGE: 5, // MB
  MODEL: 50, // MB
};

export const API_ENDPOINTS = {
  SCENES: '/scenes',
  ASSETS: '/assets',
  USERS: '/users',
  AUTH: '/auth',
};

export const ROUTES = {
  HOME: '/',
  EXPLORE: '/explore',
  CREATE: '/create',
  MARKETPLACE: '/marketplace',
  PROFILE: '/profile',
};

export const TOAST_DURATION = 5000;

export const DEFAULT_PAGINATION = {
  page: 1,
  limit: 12,
}; 