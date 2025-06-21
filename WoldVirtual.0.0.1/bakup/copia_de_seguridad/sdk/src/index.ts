/**
 * @fileoverview SDK principal de WoldVirtual Crypto 3D
 * @version 0.1.0
 * @license MIT
 */

// Core exports
export { WoldVirtualSDK } from './core/WoldVirtualSDK';
export { SceneBuilder } from './core/SceneBuilder';
export { AssetManager } from './core/AssetManager';
export { BlockchainInterface } from './core/BlockchainInterface';
export { PhysicsSystem } from './core/PhysicsSystem';
export { Networking } from './core/Networking';

// Scene management
export { Scene } from './core/Scene';
export { SceneConfig } from './core/SceneConfig';
export { SceneRenderer } from './core/SceneRenderer';
export { SceneOptimizer } from './core/SceneOptimizer';

// Asset management
export { Asset } from './core/Asset';
export { AssetLoader } from './core/AssetLoader';
export { AssetOptimizer } from './core/AssetOptimizer';
export { AssetUploader } from './core/AssetUploader';

// Blockchain integration
export { WalletManager } from './core/WalletManager';
export { NFTManager } from './core/NFTManager';
export { TransactionManager } from './core/TransactionManager';
export { SmartContractInterface } from './core/SmartContractInterface';

// Physics and interaction
export { PhysicsWorld } from './core/PhysicsWorld';
export { PhysicsBody } from './core/PhysicsBody';
export { PhysicsConstraint } from './core/PhysicsConstraint';
export { InteractionSystem } from './core/InteractionSystem';

// Networking and multiplayer
export { NetworkManager } from './core/NetworkManager';
export { PlayerManager } from './core/PlayerManager';
export { ChatSystem } from './core/ChatSystem';
export { VoiceChat } from './core/VoiceChat';

// Utilities
export { Utils } from './utils/Utils';
export { MathUtils } from './utils/MathUtils';
export { ColorUtils } from './utils/ColorUtils';
export { FileUtils } from './utils/FileUtils';
export { ValidationUtils } from './utils/ValidationUtils';

// Types
export type {
  SceneOptions,
  AssetOptions,
  PhysicsOptions,
  NetworkOptions,
  WalletOptions,
  NFTMetadata,
  TransactionOptions,
  PlayerData,
  ChatMessage,
  VoiceConfig,
} from './types';

// Constants
export {
  ASSET_TYPES,
  SCENE_TYPES,
  PHYSICS_MATERIALS,
  NETWORK_EVENTS,
  WALLET_TYPES,
  TRANSACTION_TYPES,
  DEFAULT_CONFIG,
} from './constants';

// Version info
export const VERSION = '0.1.0';
export const SDK_NAME = 'WoldVirtual SDK';

// Default configuration
export const DEFAULT_SDK_CONFIG = {
  apiUrl: 'https://api.woldvirtual.com',
  ipfsGateway: 'https://ipfs.io/ipfs/',
  blockchainNetwork: 'ethereum',
  physicsEngine: 'cannon-es',
  renderEngine: 'threejs',
  maxPlayers: 100,
  enableVoiceChat: true,
  enablePhysics: true,
  enableNetworking: true,
};

// Error types
export class WoldVirtualError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'WoldVirtualError';
  }
}

export class SceneError extends WoldVirtualError {
  constructor(message: string, code?: string) {
    super(message, code);
    this.name = 'SceneError';
  }
}

export class AssetError extends WoldVirtualError {
  constructor(message: string, code?: string) {
    super(message, code);
    this.name = 'AssetError';
  }
}

export class NetworkError extends WoldVirtualError {
  constructor(message: string, code?: string) {
    super(message, code);
    this.name = 'NetworkError';
  }
}

export class BlockchainError extends WoldVirtualError {
  constructor(message: string, code?: string) {
    super(message, code);
    this.name = 'BlockchainError';
  }
}

// Event types
export enum SDKEvents {
  SCENE_LOADED = 'scene:loaded',
  SCENE_ERROR = 'scene:error',
  ASSET_LOADED = 'asset:loaded',
  ASSET_ERROR = 'asset:error',
  PLAYER_JOINED = 'player:joined',
  PLAYER_LEFT = 'player:left',
  CHAT_MESSAGE = 'chat:message',
  VOICE_STARTED = 'voice:started',
  VOICE_STOPPED = 'voice:stopped',
  TRANSACTION_CONFIRMED = 'transaction:confirmed',
  TRANSACTION_FAILED = 'transaction:failed',
  WALLET_CONNECTED = 'wallet:connected',
  WALLET_DISCONNECTED = 'wallet:disconnected',
  NFT_MINTED = 'nft:minted',
  NFT_TRANSFERRED = 'nft:transferred',
}

// Logging utility
export class Logger {
  private static instance: Logger;
  private logLevel: 'debug' | 'info' | 'warn' | 'error' = 'info';

  static getInstance(): Logger {
    if (!Logger.instance) {
      Logger.instance = new Logger();
    }
    return Logger.instance;
  }

  setLogLevel(level: 'debug' | 'info' | 'warn' | 'error'): void {
    this.logLevel = level;
  }

  debug(message: string, ...args: any[]): void {
    if (this.logLevel === 'debug') {
      console.debug(`[${SDK_NAME}] DEBUG:`, message, ...args);
    }
  }

  info(message: string, ...args: any[]): void {
    if (['debug', 'info'].includes(this.logLevel)) {
      console.info(`[${SDK_NAME}] INFO:`, message, ...args);
    }
  }

  warn(message: string, ...args: any[]): void {
    if (['debug', 'info', 'warn'].includes(this.logLevel)) {
      console.warn(`[${SDK_NAME}] WARN:`, message, ...args);
    }
  }

  error(message: string, ...args: any[]): void {
    console.error(`[${SDK_NAME}] ERROR:`, message, ...args);
  }
}

// Global logger instance
export const logger = Logger.getInstance();

// Initialize SDK
export function initializeSDK(config: Partial<typeof DEFAULT_SDK_CONFIG> = {}): WoldVirtualSDK {
  const finalConfig = { ...DEFAULT_SDK_CONFIG, ...config };
  logger.info(`Initializing ${SDK_NAME} v${VERSION}`, finalConfig);
  return new WoldVirtualSDK(finalConfig);
}

// Export default
export default {
  WoldVirtualSDK,
  SceneBuilder,
  AssetManager,
  BlockchainInterface,
  PhysicsSystem,
  Networking,
  initializeSDK,
  VERSION,
  SDK_NAME,
  logger,
}; 