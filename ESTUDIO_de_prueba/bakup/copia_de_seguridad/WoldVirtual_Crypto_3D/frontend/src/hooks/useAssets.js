import { useState, useCallback } from 'react';
import { useToast } from '@chakra-ui/react';
import { getAssets, getAsset, createAsset } from '../utils/api';
import { handleError } from '../utils/errors';
import { validateAssetData } from '../utils/validation';
import { DEFAULT_PAGINATION } from '../utils/constants';

export const useAssets = () => {
  const [assets, setAssets] = useState([]);
  const [currentAsset, setCurrentAsset] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [pagination, setPagination] = useState(DEFAULT_PAGINATION);
  const toast = useToast();

  const fetchAssets = useCallback(async (params = {}) => {
    setIsLoading(true);
    try {
      const response = await getAssets({
        ...pagination,
        ...params,
      });
      setAssets(response.data);
      setPagination(response.pagination);
    } catch (error) {
      handleError(error, toast);
    } finally {
      setIsLoading(false);
    }
  }, [pagination, toast]);

  const fetchAsset = useCallback(async (id) => {
    setIsLoading(true);
    try {
      const response = await getAsset(id);
      setCurrentAsset(response);
    } catch (error) {
      handleError(error, toast);
    } finally {
      setIsLoading(false);
    }
  }, [toast]);

  const createNewAsset = useCallback(async (assetData) => {
    setIsLoading(true);
    try {
      const errors = validateAssetData(assetData);
      if (Object.keys(errors).length > 0) {
        throw new Error('Datos de activo inválidos');
      }

      const response = await createAsset(assetData);
      setAssets((prev) => [response, ...prev]);
      toast({
        title: 'Éxito',
        description: 'Activo creado exitosamente',
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
    assets,
    currentAsset,
    isLoading,
    pagination,
    fetchAssets,
    fetchAsset,
    createNewAsset,
    updatePagination,
  };
}; 