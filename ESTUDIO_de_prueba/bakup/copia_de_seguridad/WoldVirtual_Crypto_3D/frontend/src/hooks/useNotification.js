import { useCallback } from 'react';
import { useToast } from '@chakra-ui/react';

export const useNotification = () => {
  const toast = useToast();

  const showSuccess = useCallback((message) => {
    toast({
      title: 'Éxito',
      description: message,
      status: 'success',
      duration: 5000,
      isClosable: true,
      position: 'top-right',
    });
  }, [toast]);

  const showError = useCallback((message) => {
    toast({
      title: 'Error',
      description: message,
      status: 'error',
      duration: 5000,
      isClosable: true,
      position: 'top-right',
    });
  }, [toast]);

  const showWarning = useCallback((message) => {
    toast({
      title: 'Advertencia',
      description: message,
      status: 'warning',
      duration: 5000,
      isClosable: true,
      position: 'top-right',
    });
  }, [toast]);

  const showInfo = useCallback((message) => {
    toast({
      title: 'Información',
      description: message,
      status: 'info',
      duration: 5000,
      isClosable: true,
      position: 'top-right',
    });
  }, [toast]);

  return {
    showSuccess,
    showError,
    showWarning,
    showInfo,
  };
}; 