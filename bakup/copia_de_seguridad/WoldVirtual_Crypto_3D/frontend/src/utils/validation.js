export const isValidEthereumAddress = (address) => {
  return /^0x[a-fA-F0-9]{40}$/.test(address);
};

export const isValidEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const isValidUsername = (username) => {
  return /^[a-zA-Z0-9_]{3,20}$/.test(username);
};

export const isValidPassword = (password) => {
  return password.length >= 8;
};

export const isValidUrl = (url) => {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
};

export const isValidImageUrl = (url) => {
  if (!isValidUrl(url)) return false;
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  return imageExtensions.some((ext) => url.toLowerCase().endsWith(ext));
};

export const isValidModelUrl = (url) => {
  if (!isValidUrl(url)) return false;
  const modelExtensions = ['.glb', '.gltf'];
  return modelExtensions.some((ext) => url.toLowerCase().endsWith(ext));
};

export const validateSceneData = (data) => {
  const errors = {};

  if (!data.title) {
    errors.title = 'El título es requerido';
  } else if (data.title.length < 3) {
    errors.title = 'El título debe tener al menos 3 caracteres';
  }

  if (!data.description) {
    errors.description = 'La descripción es requerida';
  } else if (data.description.length < 10) {
    errors.description = 'La descripción debe tener al menos 10 caracteres';
  }

  if (data.imageUrl && !isValidImageUrl(data.imageUrl)) {
    errors.imageUrl = 'La URL de la imagen no es válida';
  }

  if (data.modelUrl && !isValidModelUrl(data.modelUrl)) {
    errors.modelUrl = 'La URL del modelo no es válida';
  }

  return errors;
};

export const validateAssetData = (data) => {
  const errors = {};

  if (!data.name) {
    errors.name = 'El nombre es requerido';
  } else if (data.name.length < 3) {
    errors.name = 'El nombre debe tener al menos 3 caracteres';
  }

  if (!data.description) {
    errors.description = 'La descripción es requerida';
  } else if (data.description.length < 10) {
    errors.description = 'La descripción debe tener al menos 10 caracteres';
  }

  if (!data.price) {
    errors.price = 'El precio es requerido';
  } else if (isNaN(data.price) || parseFloat(data.price) <= 0) {
    errors.price = 'El precio debe ser un número positivo';
  }

  if (data.imageUrl && !isValidImageUrl(data.imageUrl)) {
    errors.imageUrl = 'La URL de la imagen no es válida';
  }

  if (data.modelUrl && !isValidModelUrl(data.modelUrl)) {
    errors.modelUrl = 'La URL del modelo no es válida';
  }

  return errors;
}; 