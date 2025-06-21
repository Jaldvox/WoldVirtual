import { InjectedConnector } from '@web3-react/injected-connector';

export const injected = new InjectedConnector({
  supportedChainIds: [1, 3, 4, 5, 42, 56, 97, 137, 80001], // Ethereum, Ropsten, Rinkeby, Goerli, Kovan, BSC, BSC Testnet, Polygon, Mumbai
}); 