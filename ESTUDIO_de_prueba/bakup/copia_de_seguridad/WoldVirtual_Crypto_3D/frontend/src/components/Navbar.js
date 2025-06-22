import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Flex,
  HStack,
  Link,
  IconButton,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  useDisclosure,
  useColorModeValue,
  Stack,
  useColorMode,
} from '@chakra-ui/react';
import { HamburgerIcon, CloseIcon, MoonIcon, SunIcon } from '@chakra-ui/icons';
import { useWeb3React } from '@web3-react/core';
import { injected } from '../utils/connectors';

const Links = [
  { name: 'Explorar', path: '/explore' },
  { name: 'Crear', path: '/create' },
  { name: 'Marketplace', path: '/marketplace' },
];

const NavLink = ({ children, to }) => (
  <Link
    as={RouterLink}
    px={2}
    py={1}
    rounded={'md'}
    _hover={{
      textDecoration: 'none',
      bg: useColorModeValue('gray.200', 'gray.700'),
    }}
    to={to}
  >
    {children}
  </Link>
);

export default function Navbar() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { colorMode, toggleColorMode } = useColorMode();
  const { active, account, activate, deactivate } = useWeb3React();

  const connectWallet = async () => {
    try {
      await activate(injected);
    } catch (error) {
      console.log(error);
    }
  };

  const disconnectWallet = async () => {
    try {
      deactivate();
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <Box bg={useColorModeValue('gray.100', 'gray.900')} px={4} position="fixed" w="100%" zIndex={1}>
      <Flex h={16} alignItems={'center'} justifyContent={'space-between'}>
        <IconButton
          size={'md'}
          icon={isOpen ? <CloseIcon /> : <HamburgerIcon />}
          aria-label={'Open Menu'}
          display={{ md: 'none' }}
          onClick={isOpen ? onClose : onOpen}
        />
        <HStack spacing={8} alignItems={'center'}>
          <Box as={RouterLink} to="/" fontWeight="bold" fontSize="xl">
            WoldVirtual
          </Box>
          <HStack as={'nav'} spacing={4} display={{ base: 'none', md: 'flex' }}>
            {Links.map((link) => (
              <NavLink key={link.path} to={link.path}>
                {link.name}
              </NavLink>
            ))}
          </HStack>
        </HStack>
        <Flex alignItems={'center'}>
          <Button onClick={toggleColorMode} mr={4}>
            {colorMode === 'light' ? <MoonIcon /> : <SunIcon />}
          </Button>
          {active ? (
            <Menu>
              <MenuButton as={Button} rounded={'full'} variant={'link'} cursor={'pointer'}>
                {`${account.substring(0, 6)}...${account.substring(account.length - 4)}`}
              </MenuButton>
              <MenuList>
                <MenuItem as={RouterLink} to="/profile">Perfil</MenuItem>
                <MenuItem onClick={disconnectWallet}>Desconectar</MenuItem>
              </MenuList>
            </Menu>
          ) : (
            <Button onClick={connectWallet}>Conectar Wallet</Button>
          )}
        </Flex>
      </Flex>

      {isOpen ? (
        <Box pb={4} display={{ md: 'none' }}>
          <Stack as={'nav'} spacing={4}>
            {Links.map((link) => (
              <NavLink key={link.path} to={link.path}>
                {link.name}
              </NavLink>
            ))}
          </Stack>
        </Box>
      ) : null}
    </Box>
  );
} 