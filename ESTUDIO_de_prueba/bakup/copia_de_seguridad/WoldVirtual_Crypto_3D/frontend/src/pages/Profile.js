import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  Stack,
  SimpleGrid,
  Avatar,
  Button,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  useColorModeValue,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
} from '@chakra-ui/react';
import { useWeb3React } from '@web3-react/core';
import SceneCard from '../components/SceneCard';
import AssetCard from '../components/AssetCard';

// Datos de ejemplo
const mockUserData = {
  username: 'Usuario123',
  avatarUrl: 'https://via.placeholder.com/150',
  walletAddress: '0x1234...5678',
  joinDate: '2024-01-01',
  stats: {
    scenesCreated: 5,
    assetsOwned: 12,
    totalSales: '2.5 ETH',
    reputation: 85,
  },
};

const mockUserScenes = [
  {
    id: 1,
    title: 'Mi Mundo Virtual',
    description: 'Un mundo virtual personalizado',
    creator: mockUserData.walletAddress,
    imageUrl: 'https://via.placeholder.com/300x200',
    likes: 123,
    visits: 456,
  },
  // Añade más escenas de ejemplo aquí
];

const mockUserAssets = [
  {
    id: 1,
    name: 'Mi Activo Digital',
    description: 'Un activo digital personalizado',
    creator: mockUserData.walletAddress,
    imageUrl: 'https://via.placeholder.com/300x200',
    price: '0.5 ETH',
    category: 'buildings',
  },
  // Añade más activos de ejemplo aquí
];

export default function Profile() {
  const { active, account } = useWeb3React();
  const [isEditing, setIsEditing] = useState(false);

  if (!active) {
    return (
      <Container maxW={'7xl'} py={12}>
        <Stack spacing={8} align="center">
          <Heading>Conecta tu Wallet</Heading>
          <Text>Por favor, conecta tu wallet para ver tu perfil.</Text>
        </Stack>
      </Container>
    );
  }

  return (
    <Container maxW={'7xl'} py={12}>
      <Stack spacing={8}>
        <Box
          bg={useColorModeValue('white', 'gray.700')}
          p={8}
          rounded={'lg'}
          boxShadow={'lg'}
        >
          <Stack direction={{ base: 'column', md: 'row' }} spacing={8} align="center">
            <Avatar size="2xl" src={mockUserData.avatarUrl} />
            <Stack spacing={4} flex={1}>
              <Heading size="lg">{mockUserData.username}</Heading>
              <Text>Wallet: {mockUserData.walletAddress}</Text>
              <Text>Miembro desde: {mockUserData.joinDate}</Text>
              <Button
                colorScheme="brand"
                onClick={() => setIsEditing(!isEditing)}
                alignSelf="flex-start"
              >
                {isEditing ? 'Guardar Cambios' : 'Editar Perfil'}
              </Button>
            </Stack>
          </Stack>

          <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6} mt={8}>
            <Stat>
              <StatLabel>Escenas Creadas</StatLabel>
              <StatNumber>{mockUserData.stats.scenesCreated}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                23.36%
              </StatHelpText>
            </Stat>
            <Stat>
              <StatLabel>Activos Poseídos</StatLabel>
              <StatNumber>{mockUserData.stats.assetsOwned}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                9.05%
              </StatHelpText>
            </Stat>
            <Stat>
              <StatLabel>Ventas Totales</StatLabel>
              <StatNumber>{mockUserData.stats.totalSales}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                12.5%
              </StatHelpText>
            </Stat>
            <Stat>
              <StatLabel>Reputación</StatLabel>
              <StatNumber>{mockUserData.stats.reputation}</StatNumber>
              <StatHelpText>
                <StatArrow type="increase" />
                5.2%
              </StatHelpText>
            </Stat>
          </SimpleGrid>
        </Box>

        <Tabs variant="enclosed">
          <TabList>
            <Tab>Mis Escenas</Tab>
            <Tab>Mis Activos</Tab>
            <Tab>Actividad</Tab>
          </TabList>

          <TabPanels>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {mockUserScenes.map((scene) => (
                  <SceneCard key={scene.id} scene={scene} />
                ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {mockUserAssets.map((asset) => (
                  <AssetCard key={asset.id} asset={asset} />
                ))}
              </SimpleGrid>
            </TabPanel>
            <TabPanel>
              <Stack spacing={4}>
                <Text>No hay actividad reciente.</Text>
              </Stack>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Stack>
    </Container>
  );
} 