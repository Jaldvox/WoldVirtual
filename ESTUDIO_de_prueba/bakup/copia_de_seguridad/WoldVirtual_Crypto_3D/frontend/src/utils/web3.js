import { ethers } from 'ethers';

export const formatAddress = (address) => {
  if (!address) return '';
  return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`;
};

export const formatBalance = (balance) => {
  if (!balance) return '0';
  return ethers.utils.formatEther(balance);
};

export const parseEther = (amount) => {
  return ethers.utils.parseEther(amount.toString());
};

export const getContract = (address, abi, signer) => {
  return new ethers.Contract(address, abi, signer);
};

export const getProvider = () => {
  return new ethers.providers.Web3Provider(window.ethereum);
};

export const getSigner = (provider) => {
  return provider.getSigner();
}; 