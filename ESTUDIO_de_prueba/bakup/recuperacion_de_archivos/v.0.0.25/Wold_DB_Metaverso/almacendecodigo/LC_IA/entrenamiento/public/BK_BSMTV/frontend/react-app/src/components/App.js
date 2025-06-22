import React from 'react';
import User from './User';
import './styles.css';

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Administración de Usuarios</h1>
            </header>
            <main>
                <User />
            </main>
        </div>
    );
};

export default App;