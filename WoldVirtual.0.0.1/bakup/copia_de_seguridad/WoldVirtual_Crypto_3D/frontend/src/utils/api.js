import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const setAuthToken = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

export const getScenes = async () => {
  try {
    const response = await api.get('/scenes');
    return response.data;
  } catch (error) {
    console.error('Error fetching scenes:', error);
    throw error;
  }
};

export const getScene = async (id) => {
  try {
    const response = await api.get(`/scenes/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching scene:', error);
    throw error;
  }
};

export const createScene = async (sceneData) => {
  try {
    const response = await api.post('/scenes', sceneData);
    return response.data;
  } catch (error) {
    console.error('Error creating scene:', error);
    throw error;
  }
};

export const getAssets = async () => {
  try {
    const response = await api.get('/assets');
    return response.data;
  } catch (error) {
    console.error('Error fetching assets:', error);
    throw error;
  }
};

export const getAsset = async (id) => {
  try {
    const response = await api.get(`/assets/${id}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching asset:', error);
    throw error;
  }
};

export const createAsset = async (assetData) => {
  try {
    const response = await api.post('/assets', assetData);
    return response.data;
  } catch (error) {
    console.error('Error creating asset:', error);
    throw error;
  }
};

export const getUserProfile = async (address) => {
  try {
    const response = await api.get(`/users/${address}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export const updateUserProfile = async (address, profileData) => {
  try {
    const response = await api.put(`/users/${address}`, profileData);
    return response.data;
  } catch (error) {
    console.error('Error updating user profile:', error);
    throw error;
  }
}; 