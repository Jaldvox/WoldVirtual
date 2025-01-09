import React from 'react';

const User = ({ user }) => {
    return (
        <div className="user-card">
            <h2>{user.name}</h2>
            <p>Email: {user.email}</p>
            <p>Rol: {user.role}</p>
        </div>
    );
};

export default User;