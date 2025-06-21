import React from 'react';
import {
  Box,
  Image,
  Badge,
  Text,
  Stack,
  Button,
  useColorModeValue,
  Heading,
} from '@chakra-ui/react';
import { useWeb3React } from '@web3-react/core';
import { useToast } from '@chakra-ui/react';

const AssetCard = ({ asset }) => {
  const { active } = useWeb3React();
  const toast = useToast();

  const handleBuy = async () => {
    if (!active) {
      toast({
        title: 'Error',
        description: 'Por favor, conecta tu wallet primero',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    try {
      // Aquí iría la lógica para comprar el activo
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulación de transacción
      toast({
        title: 'Éxito',
        description: 'Has comprado el activo exitosamente',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Hubo un error al comprar el activo',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  return (
    <Box
      maxW={'sm'}
      w={'full'}
      bg={useColorModeValue('white', 'gray.800')}
      boxShadow={'2xl'}
      rounded={'md'}
      overflow={'hidden'}
    >
      <Image
        h={'200px'}
        w={'full'}
        src={asset.imageUrl}
        objectFit={'cover'}
        alt={asset.name}
      />

      <Box p={6}>
        <Stack spacing={0} align={'center'} mb={5}>
          <Heading fontSize={'2xl'} fontWeight={500} fontFamily={'body'}>
            {asset.name}
          </Heading>
          <Text color={'gray.500'}>{asset.description}</Text>
        </Stack>

        <Stack direction={'row'} justify={'center'} spacing={6}>
          <Stack spacing={0} align={'center'}>
            <Text fontWeight={600}>{asset.price}</Text>
          </Stack>
        </Stack>

        <Stack align={'center'} justify={'center'} direction={'row'} mt={6}>
          <Badge
            px={2}
            py={1}
            bg={useColorModeValue('gray.50', 'gray.800')}
            fontWeight={'400'}
          >
            Creador: {asset.creator}
          </Badge>
        </Stack>

        <Button
          w={'full'}
          mt={8}
          bg={useColorModeValue('brand.500', 'brand.900')}
          color={'white'}
          rounded={'md'}
          _hover={{
            transform: 'translateY(-2px)',
            boxShadow: 'lg',
          }}
          onClick={handleBuy}
        >
          Comprar
        </Button>
      </Box>
    </Box>
  );
};

export default AssetCard; 