import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Container,
  Heading,
  Text,
  Stack,
  SimpleGrid,
  Icon,
  useColorModeValue,
} from '@chakra-ui/react';
import { FaCube, FaStore, FaUserPlus } from 'react-icons/fa';

const Feature = ({ title, text, icon }) => {
  return (
    <Stack
      align={'center'}
      textAlign={'center'}
      p={6}
      bg={useColorModeValue('white', 'gray.800')}
      rounded={'xl'}
      boxShadow={'lg'}
    >
      <Icon as={icon} w={10} h={10} color={'brand.500'} />
      <Text fontWeight={600}>{title}</Text>
      <Text color={useColorModeValue('gray.600', 'gray.400')}>{text}</Text>
    </Stack>
  );
};

export default function Home() {
  return (
    <Container maxW={'7xl'}>
      <Stack
        as={Box}
        textAlign={'center'}
        spacing={{ base: 8, md: 14 }}
        py={{ base: 20, md: 36 }}
      >
        <Heading
          fontWeight={600}
          fontSize={{ base: '2xl', sm: '4xl', md: '6xl' }}
          lineHeight={'110%'}
        >
          Bienvenido a <br />
          <Text as={'span'} color={'brand.500'}>
            WoldVirtual
          </Text>
        </Heading>
        <Text color={'gray.500'}>
          El primer metaverso descentralizado 3D donde puedes crear, explorar y monetizar tus
          experiencias virtuales.
        </Text>
        <Stack
          direction={'column'}
          spacing={3}
          align={'center'}
          alignSelf={'center'}
          position={'relative'}
        >
          <Button
            as={RouterLink}
            to="/explore"
            colorScheme={'brand'}
            bg={'brand.500'}
            rounded={'full'}
            px={6}
            _hover={{
              bg: 'brand.600',
            }}
          >
            Explorar Ahora
          </Button>
        </Stack>
      </Stack>

      <SimpleGrid columns={{ base: 1, md: 3 }} spacing={10} py={10}>
        <Feature
          icon={FaCube}
          title={'Crear'}
          text={'Crea tus propios mundos virtuales y experiencias 3D personalizadas.'}
        />
        <Feature
          icon={FaStore}
          title={'Marketplace'}
          text={'Compra y vende activos digitales en nuestro marketplace descentralizado.'}
        />
        <Feature
          icon={FaUserPlus}
          title={'Comunidad'}
          text={'Únete a una comunidad global de creadores y exploradores.'}
        />
      </SimpleGrid>
    </Container>
  );
} 