import { useState, useCallback } from 'react';
import { useToast } from '@chakra-ui/react';
import { getScenes, getScene, createScene } from '../utils/api';
import { handleError } from '../utils/errors';
import { validateSceneData } from '../utils/validation';
import { DEFAULT_PAGINATION } from '../utils/constants';

export const useScenes = () => {
  const [scenes, setScenes] = useState([]);
  const [currentScene, setCurrentScene] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [pagination, setPagination] = useState(DEFAULT_PAGINATION);
  const toast = useToast();

  const fetchScenes = useCallback(async (params = {}) => {
    setIsLoading(true);
    try {
      const response = await getScenes({
        ...pagination,
        ...params,
      });
      setScenes(response.data);
      setPagination(response.pagination);
    } catch (error) {
      handleError(error, toast);
    } finally {
      setIsLoading(false);
    }
  }, [pagination, toast]);

  const fetchScene = useCallback(async (id) => {
    setIsLoading(true);
    try {
      const response = await getScene(id);
      setCurrentScene(response);
    } catch (error) {
      handleError(error, toast);
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  const createNewScene = useCallback(async (sceneData) => {
    setIsLoading(true);
    try {
      const errors = validateSceneData(sceneData);
      if (Object.keys(errors).length > 0) {
        throw new Error('Datos de escena inválidos');
      }

      const response = await createScene(sceneData);
      setScenes((prev) => [response, ...prev]);
      toast({
        title: 'Éxito',
        description: 'Escena creada exitosamente',
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

  const updatePagination = useCallback((newPagination) => {
    setPagination((prev) => ({
      ...prev,
      ...newPagination,
    }));
  }, []);

  return {
    scenes,
    currentScene,
    isLoading,
    pagination,
    fetchScenes,
    fetchScene,
    createNewScene,
    updatePagination,
  };
}; 