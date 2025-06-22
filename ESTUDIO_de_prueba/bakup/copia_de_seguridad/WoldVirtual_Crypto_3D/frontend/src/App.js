import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@chakra-ui/react';

// Componentes
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Explore from './pages/Explore';
import Create from './pages/Create';
import Marketplace from './pages/Marketplace';
import Profile from './pages/Profile';

function App() {
  return (
    <Box minH="100vh">
      <Navbar />
      <Box as="main" pt="16">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/explore" element={<Explore />} />
          <Route path="/create" element={<Create />} />
          <Route path="/marketplace" element={<Marketplace />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App; 