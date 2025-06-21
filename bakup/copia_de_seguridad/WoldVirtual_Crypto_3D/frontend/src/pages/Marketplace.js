import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Input,
  InputGroup,
  InputLeftElement,
  Select,
  Stack,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useColorModeValue,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';
import AssetCard from '../components/AssetCard';

// Datos de ejemplo
const mockAssets = [
  {
    id: 1,
    name: 'Edificio Futurista',
    description: 'Modelo 3D de un edificio futurista',
    creator: '0x1234...5678',
    imageUrl: 'https://via.placeholder.com/300x200',
    price: '0.5 ETH',
    category: 'buildings',
  },
  {
    id: 2,
    name: 'Árbol Mágico',
    description: 'Modelo 3D de un árbol mágico animado',
    creator: '0x8765...4321',
    imageUrl: 'https://via.placeholder.com/300x200',
    price: '0.2 ETH',
    category: 'nature',
  },
  // Añade más activos de ejemplo aquí
];

export default function Marketplace() {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('price-asc');

  const filteredAssets = mockAssets.filter((asset) =>
    asset.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Container maxW={'7xl'} py={12}>
      <Stack spacing={8}>
        <Heading textAlign={'center'}>Marketplace</Heading>

        <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
          <InputGroup>
            <InputLeftElement pointerEvents="none">
              <SearchIcon color="gray.300" />
            </InputLeftElement>
            <Input
              placeholder="Buscar activos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </InputGroup>

          <Select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            maxW={{ base: 'full', md: '200px' }}
          >
            <option value="price-asc">Precio: Menor a Mayor</option>
            <option value="price-desc">Precio: Mayor a Menor</option>
            <option value="recent">Más Recientes</option>
          </Select>
        </Stack>

        <Tabs variant="enclosed">
          <TabList>
            <Tab>Todos</Tab>
            <Tab>Edificios</Tab>
            <Tab>Naturaleza</Tab>
            <Tab>Personajes</Tab>
            <Tab>Efectos</Tab>
          </TabList>

          <TabPanels>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {filteredAssets.map((asset) => (
                  <AssetCard key={asset.id} asset={asset} />
                ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {filteredAssets
                  .filter((asset) => asset.category === 'buildings')
                  .map((asset) => (
                    <AssetCard key={asset.id} asset={asset} />
                  ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {filteredAssets
                  .filter((asset) => asset.category === 'nature')
                  .map((asset) => (
                    <AssetCard key={asset.id} asset={asset} />
                  ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {filteredAssets
                  .filter((asset) => asset.category === 'characters')
                  .map((asset) => (
                    <AssetCard key={asset.id} asset={asset} />
                  ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {filteredAssets
                  .filter((asset) => asset.category === 'effects')
                  .map((asset) => (
                    <AssetCard key={asset.id} asset={asset} />
                  ))}
              </SimpleGrid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Stack>
    </Container>
  );
} 