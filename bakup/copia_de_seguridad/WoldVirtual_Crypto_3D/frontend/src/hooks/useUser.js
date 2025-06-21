import { useState, useCallback } from 'react';
import { useToast } from '@chakra-ui/react';
import { getUserProfile, updateUserProfile } from '../utils/api';
import { handleError } from '../utils/errors';
import { isValidUsername, isValidEmail } from '../utils/validation';

export const useUser = () => {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const fetchUserProfile = useCallback(async (address) => {
    setIsLoading(true);
    try {
      const response = await getUserProfile(address);
      setUser(response);
    } catch (error) {
      handleError(error, toast);
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  const updateProfile = useCallback(async (address, profileData) => {
    setIsLoading(true);
    try {
      // Validar datos del perfil
      if (profileData.username && !isValidUsername(profileData.username)) {
        throw new Error('Nombre de usuario inválido');
      }
      if (profileData.email && !isValidEmail(profileData.email)) {
        throw new Error('Email inválido');
      }

      const response = await updateUserProfile(address, profileData);
      setUser(response);
      toast({
        title: 'Éxito',
        description: 'Perfil actualizado exitosamente',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      return response;
    } catch (error) {
      handleError(error, toast);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  const clearUser = useCallback(() => {
    setUser(null);
  }, []);

  return {
    user,
    isLoading,
    fetchUserProfile,
    updateProfile,
    clearUser,
  };
}; 