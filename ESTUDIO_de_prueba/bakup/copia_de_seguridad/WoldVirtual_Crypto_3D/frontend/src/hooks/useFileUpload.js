import { useState, useCallback } from 'react';
import { useToast } from '@chakra-ui/react';
import {
  validateFileType,
  validateFileSize,
  readFileAsDataURL,
  readFileAsArrayBuffer,
} from '../utils/files';
import { FILE_TYPES, MAX_FILE_SIZES } from '../utils/constants';
import { handleError } from '../utils/errors';

export const useFileUpload = () => {
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const toast = useToast();

  const validateFile = useCallback((file, type) => {
    if (!validateFileType(file, FILE_TYPES[type])) {
      throw new Error(`Tipo de archivo no válido. Tipos permitidos: ${FILE_TYPES[type].join(', ')}`);
    }

    if (!validateFileSize(file, MAX_FILE_SIZES[type])) {
      throw new Error(`El archivo es demasiado grande. Tamaño máximo: ${MAX_FILE_SIZES[type]}MB`);
    }
  }, []);

  const uploadFile = useCallback(async (file, type, onUploadComplete) => {
    setIsUploading(true);
    setUploadProgress(0);

    try {
      // Validar archivo
      validateFile(file, type);

      // Simular progreso de carga
      const progressInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return prev;
          }
          return prev + 10;
        });
      }, 500);

      // Leer archivo según el tipo
      let fileData;
      if (type === 'IMAGE') {
        fileData = await readFileAsDataURL(file);
      } else {
        fileData = await readFileAsArrayBuffer(file);
      }

      // Simular carga al servidor
      await new Promise((resolve) => setTimeout(resolve, 2000));

      clearInterval(progressInterval);
      setUploadProgress(100);

      // Llamar al callback de completado
      if (onUploadComplete) {
        await onUploadComplete(fileData);
      }

      toast({
        title: 'Éxito',
        description: 'Archivo subido exitosamente',
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      return fileData;
    } catch (error) {
      handleError(error, toast);
      throw error;
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  }, [validateFile, toast]);

  return {
    isUploading,
    uploadProgress,
    uploadFile,
  };
}; 