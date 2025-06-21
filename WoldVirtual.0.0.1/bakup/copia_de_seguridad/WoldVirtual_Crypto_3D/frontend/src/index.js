import React from 'react';
import ReactDOM from 'react-dom/client';
import { ChakraProvider } from '@chakra-ui/react';
import { Web3ReactProvider } from '@web3-react/core';
import { ethers } from 'ethers';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import theme from './theme';

function getLibrary(provider) {
  return new ethers.providers.Web3Provider(provider);
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Web3ReactProvider getLibrary={getLibrary}>
      <ChakraProvider theme={theme}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ChakraProvider>
    </Web3ReactProvider>
  </React.StrictMode>
); 