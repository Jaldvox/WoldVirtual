import { useState, useEffect, useCallback } from 'react';
import { useWeb3React } from '@web3-react/core';
import { injected } from '../utils/connectors';
import { SUPPORTED_CHAINS, CHAIN_NAMES, CHAIN_CURRENCIES } from '../utils/constants';
import { formatBalance } from '../utils/web3';

export const useWallet = () => {
  const { active, account, library, chainId, activate, deactivate } = useWeb3React();
  const [balance, setBalance] = useState('0');
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState(null);

  const connect = useCallback(async () => {
    setIsConnecting(true);
    setError(null);
    try {
      await activate(injected);
    } catch (error) {
      console.error('Error connecting wallet:', error);
      setError('Error al conectar la wallet');
    } finally {
      setIsConnecting(false);
    }
  }, [activate]);

  const disconnect = useCallback(async () => {
    try {
      deactivate();
    } catch (error) {
      console.error('Error disconnecting wallet:', error);
      setError('Error al desconectar la wallet');
    }
  }, [deactivate]);

  const switchChain = useCallback(async (targetChainId) => {
    if (!library?.provider?.request) return;

    try {
      await library.provider.request({
        method: 'wallet_switchEthereumChain',
        params: [{ chainId: `0x${targetChainId.toString(16)}` }],
      });
    } catch (error) {
      console.error('Error switching chain:', error);
      setError('Error al cambiar de red');
    }
  }, [library]);

  useEffect(() => {
    const getBalance = async () => {
      if (active && account && library) {
        try {
          const balance = await library.getBalance(account);
          setBalance(formatBalance(balance));
        } catch (error) {
          console.error('Error getting balance:', error);
          setBalance('0');
        }
      }
    };

    getBalance();
    const interval = setInterval(getBalance, 10000); // Actualizar cada 10 segundos

    return () => clearInterval(interval);
  }, [active, account, library]);

  const isSupportedChain = chainId ? Object.values(SUPPORTED_CHAINS).includes(chainId) : false;
  const chainName = chainId ? CHAIN_NAMES[chainId] : null;
  const chainCurrency = chainId ? CHAIN_CURRENCIES[chainId] : null;

  return {
    active,
    account,
    chainId,
    chainName,
    chainCurrency,
    balance,
    isConnecting,
    error,
    isSupportedChain,
    connect,
    disconnect,
    switchChain,
  };
}; 