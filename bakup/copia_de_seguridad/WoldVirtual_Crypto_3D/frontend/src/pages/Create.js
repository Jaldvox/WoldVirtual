import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Textarea,
  Button,
  VStack,
  useToast,
  useColorModeValue,
} from '@chakra-ui/react';
import { useWeb3React } from '@web3-react/core';

export default function Create() {
  const { active } = useWeb3React();
  const toast = useToast();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    imageUrl: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
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

    setIsLoading(true);
    try {
      // Aquí iría la lógica para crear la escena
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulación de llamada API
      toast({
        title: 'Éxito',
        description: 'Tu mundo virtual ha sido creado',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      setFormData({ title: '', description: '', imageUrl: '' });
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Hubo un error al crear tu mundo virtual',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container maxW={'container.md'} py={12}>
      <VStack spacing={8} align="stretch">
        <Heading textAlign={'center'}>Crear Mundo Virtual</Heading>

        <Box
          as="form"
          onSubmit={handleSubmit}
          bg={useColorModeValue('white', 'gray.700')}
          p={8}
          rounded={'lg'}
          boxShadow={'lg'}
        >
          <VStack spacing={4}>
            <FormControl isRequired>
              <FormLabel>Título</FormLabel>
              <Input
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                placeholder="Nombre de tu mundo virtual"
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel>Descripción</FormLabel>
              <Textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                placeholder="Describe tu mundo virtual"
                rows={4}
              />
            </FormControl>

            <FormControl isRequired>
              <FormLabel>URL de la Imagen</FormLabel>
              <Input
                name="imageUrl"
                value={formData.imageUrl}
                onChange={handleInputChange}
                placeholder="URL de la imagen de portada"
              />
            </FormControl>

            <Button
              type="submit"
              colorScheme={'brand'}
              size={'lg'}
              width={'full'}
              isLoading={isLoading}
              loadingText="Creando..."
            >
              Crear Mundo Virtual
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
} 