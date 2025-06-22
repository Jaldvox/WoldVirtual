import { useState, useCallback } from 'react';

/**
 * Hook para gestión de usuario usando los endpoints REST del backend Reflex.
 * Permite obtener y actualizar perfil, avatar, inventario y estado.
 */
export function useUser() {
  const [user, setUser] = useState(null);
  const [privateProfile, setPrivateProfile] = useState(null);
  const [loading, setLoading] = useState(false);

  // Obtener perfil público
  const fetchPublicProfile = useCallback(async () => {
    setLoading(true);
    const res = await fetch('/api/get_user_public_profile');
    setUser(await res.json());
    setLoading(false);
  }, []);

  // Obtener perfil privado
  const fetchPrivateProfile = useCallback(async () => {
    setLoading(true);
    const res = await fetch('/api/get_user_private_profile');
    setPrivateProfile(await res.json());
    setLoading(false);
  }, []);

  // Actualizar avatar
  const updateAvatar = useCallback(async (avatarUrl) => {
    setLoading(true);
    await fetch('/api/update_user_avatar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ avatar_url: avatarUrl }),
    });
    await fetchPublicProfile();
    setLoading(false);
  }, [fetchPublicProfile]);

  // Añadir asset
  const addAsset = useCallback(async (assetId) => {
    setLoading(true);
    await fetch('/api/add_asset_to_user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asset_id: assetId }),
    });
    await fetchPrivateProfile();
    setLoading(false);
  }, [fetchPrivateProfile]);

  // Eliminar asset
  const removeAsset = useCallback(async (assetId) => {
    setLoading(true);
    await fetch('/api/remove_asset_from_user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ asset_id: assetId }),
    });
    await fetchPrivateProfile();
    setLoading(false);
  }, [fetchPrivateProfile]);

  // Cambiar estado
  const setStatus = useCallback(async (estado) => {
    setLoading(true);
    await fetch('/api/set_user_status', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ estado }),
    });
    await fetchPublicProfile();
    setLoading(false);
  }, [fetchPublicProfile]);

  return {
    user,
    privateProfile,
    loading,
    fetchPublicProfile,
    fetchPrivateProfile,
    updateAvatar,
    addAsset,
    removeAsset,
    setStatus,
  };
} 