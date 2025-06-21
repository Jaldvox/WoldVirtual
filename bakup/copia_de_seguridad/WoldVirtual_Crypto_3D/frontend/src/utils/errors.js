export class AppError extends Error {
  constructor(message, code, details = null) {
    super(message);
    this.name = 'AppError';
    this.code = code;
    this.details = details;
  }
}

export const handleError = (error, toast) => {
  console.error('Error:', error);

  if (error instanceof AppError) {
    toast({
      title: 'Error',
      description: error.message,
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
    return;
  }

  if (error.response) {
    // Error de respuesta del servidor
    const { data, status } = error.response;
    toast({
      title: `Error ${status}`,
      description: data.message || 'Ha ocurrido un error en el servidor',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
    return;
  }

  if (error.request) {
    // Error de red
    toast({
      title: 'Error de Conexión',
      description: 'No se pudo conectar con el servidor',
      status: 'error',
      duration: 5000,
      isClosable: true,
    });
    return;
  }

  // Error general
  toast({
    title: 'Error',
    description: 'Ha ocurrido un error inesperado',
    status: 'error',
    duration: 5000,
    isClosable: true,
  });
};

export const isNetworkError = (error) => {
  return error.message === 'Network Error';
};

export const isAuthError = (error) => {
  return error.response?.status === 401;
};

export const isValidationError = (error) => {
  return error.response?.status === 422;
};

export const isServerError = (error) => {
  return error.response?.status >= 500;
}; 