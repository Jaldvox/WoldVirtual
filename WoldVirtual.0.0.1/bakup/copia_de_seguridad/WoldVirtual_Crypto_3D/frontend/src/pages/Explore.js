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
  useColorModeValue,
} from '@chakra-ui/react';
import { SearchIcon } from '@chakra-ui/icons';
import SceneCard from '../components/SceneCard';

// Datos de ejemplo
const mockScenes = [
  {
    id: 1,
    title: 'Ciudad Futurista',
    description: 'Explora una metrópolis del futuro con tecnología avanzada.',
    creator: '0x1234...5678',
    imageUrl: 'https://via.placeholder.com/300x200',
    likes: 1234,
    visits: 5678,
  },
  {
    id: 2,
    title: 'Bosque Mágico',
    description: 'Un bosque encantado lleno de criaturas mágicas y secretos.',
    creator: '0x8765...4321',
    imageUrl: 'https://via.placeholder.com/300x200',
    likes: 876,
    visits: 2345,
  },
  // Añade más escenas de ejemplo aquí
];

export default function Explore() {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('popular');

  const filteredScenes = mockScenes.filter((scene) =>
    scene.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Container maxW={'7xl'} py={12}>
      <Stack spacing={8}>
        <Heading textAlign={'center'}>Explorar Mundos Virtuales</Heading>

        <Stack direction={{ base: 'column', md: 'row' }} spacing={4}>
          <InputGroup>
            <InputLeftElement pointerEvents="none">
              <SearchIcon color="gray.300" />
            </InputLeftElement>
            <Input
              placeholder="Buscar mundos..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </InputGroup>

          <Select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            maxW={{ base: 'full', md: '200px' }}
          >
            <option value="popular">Más Populares</option>
            <option value="recent">Más Recientes</option>
            <option value="visits">Más Visitados</option>
          </Select>
        </Stack>

        <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
          {filteredScenes.map((scene) => (
            <SceneCard key={scene.id} scene={scene} />
          ))}
        </SimpleGrid>
      </Stack>
    </Container>
  );
} 