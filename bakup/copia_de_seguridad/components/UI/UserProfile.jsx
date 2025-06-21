import React, { useEffect, useState } from 'react';
import { useUser } from '../../hooks/useUser';

/**
 * Componente de perfil de usuario.
 * Permite ver y editar avatar, estado e inventario usando los endpoints REST del backend Reflex.
 */
export default function UserProfile() {
  const {
    user,
    privateProfile,
    loading,
    fetchPublicProfile,
    fetchPrivateProfile,
    updateAvatar,
    addAsset,
    removeAsset,
    setStatus,
  } = useUser();

  const [avatarInput, setAvatarInput] = useState('');
  const [assetInput, setAssetInput] = useState('');

  useEffect(() => {
    fetchPublicProfile();
    fetchPrivateProfile();
  }, [fetchPublicProfile, fetchPrivateProfile]);

  if (loading || !user) return <div>Cargando perfil...</div>;

  return (
    <div style={{ border: '1px solid #ccc', borderRadius: 8, padding: 24, maxWidth: 400 }}>
      <h2>Perfil de Usuario</h2>
      <img src={user.avatar_url} alt="Avatar" width={100} style={{ borderRadius: '50%' }} />
      <div><strong>Usuario:</strong> {user.username}</div>
      <div><strong>Estado:</strong> {user.estado}
        <button onClick={() => setStatus('conectado')}>Conectado</button>
        <button onClick={() => setStatus('ausente')}>Ausente</button>
      </div>
      <div style={{ margin: '8px 0' }}>
        <input
          type="text"
          placeholder="Nueva URL de avatar"
          value={avatarInput}
          onChange={e => setAvatarInput(e.target.value)}
        />
        <button onClick={() => updateAvatar(avatarInput)}>Actualizar Avatar</button>
      </div>
      <div>
        <h3>Inventario</h3>
        {privateProfile && privateProfile.owned_assets.length === 0 && <div>No tienes assets.</div>}
        {privateProfile && privateProfile.owned_assets.map(assetId => (
          <div key={assetId} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            {assetId}
            <button onClick={() => removeAsset(assetId)}>Eliminar</button>
          </div>
        ))}
        <div style={{ marginTop: 8 }}>
          <input
            type="text"
            placeholder="ID de asset a añadir"
            value={assetInput}
            onChange={e => setAssetInput(e.target.value)}
          />
          <button onClick={() => { addAsset(assetInput); setAssetInput(''); }}>Añadir Asset</button>
        </div>
      </div>
    </div>
  );
} 