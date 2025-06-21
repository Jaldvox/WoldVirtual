import { useCallback } from 'react';
import { useColorMode, useColorModeValue } from '@chakra-ui/react';

export const useTheme = () => {
  const { colorMode, toggleColorMode } = useColorMode();

  const isDark = colorMode === 'dark';

  const bgColor = useColorModeValue('white', 'gray.800');
  const textColor = useColorModeValue('gray.800', 'white');
  const borderColor = useColorModeValue('gray.200', 'gray.700');
  const hoverBgColor = useColorModeValue('gray.50', 'gray.700');
  const cardBgColor = useColorModeValue('white', 'gray.700');
  const inputBgColor = useColorModeValue('white', 'gray.700');
  const buttonBgColor = useColorModeValue('brand.500', 'brand.900');
  const buttonHoverBgColor = useColorModeValue('brand.600', 'brand.800');

  const toggleTheme = useCallback(() => {
    toggleColorMode();
  }, [toggleColorMode]);

  return {
    isDark,
    colorMode,
    bgColor,
    textColor,
    borderColor,
    hoverBgColor,
    cardBgColor,
    inputBgColor,
    buttonBgColor,
    buttonHoverBgColor,
    toggleTheme,
  };
}; 