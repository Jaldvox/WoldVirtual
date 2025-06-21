import React from 'react';
import {
  Box,
  Image,
  Badge,
  Text,
  Stack,
  Flex,
  Icon,
  useColorModeValue,
  Heading,
} from '@chakra-ui/react';
import { FaHeart, FaEye } from 'react-icons/fa';

const SceneCard = ({ scene }) => {
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
        src={scene.imageUrl}
        objectFit={'cover'}
        alt={scene.title}
      />

      <Box p={6}>
        <Stack spacing={0} align={'center'} mb={5}>
          <Heading fontSize={'2xl'} fontWeight={500} fontFamily={'body'}>
            {scene.title}
          </Heading>
          <Text color={'gray.500'}>{scene.description}</Text>
        </Stack>

        <Stack direction={'row'} justify={'center'} spacing={6}>
          <Stack spacing={0} align={'center'}>
            <Icon as={FaHeart} color={'red.500'} />
            <Text fontWeight={600}>{scene.likes}</Text>
          </Stack>
          <Stack spacing={0} align={'center'}>
            <Icon as={FaEye} color={'blue.500'} />
            <Text fontWeight={600}>{scene.visits}</Text>
          </Stack>
        </Stack>

        <Stack align={'center'} justify={'center'} direction={'row'} mt={6}>
          <Badge
            px={2}
            py={1}
            bg={useColorModeValue('gray.50', 'gray.800')}
            fontWeight={'400'}
          >
            Creador: {scene.creator}
          </Badge>
        </Stack>
      </Box>
    </Box>
  );
};

export default SceneCard; 