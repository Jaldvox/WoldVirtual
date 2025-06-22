
# React + Vite Setup Guide for Reflex Complement

## Prerequisites

- Node.js (version 18 or higher)
- npm or yarn package manager
- Git (optional but recommended)

## Installation Steps

### 1. Create a New Vite Project with React

```bash
# Create project with Vite
npm create vite@latest my-reflex-complement -- --template react

# Navigate to project directory
cd my-reflex-complement
```

### 2. Install Dependencies

```bash
# Install base dependencies
npm install

# Install additional dependencies for Reflex integration
npm install axios react-router-dom
```

### 3. Development Dependencies (Optional)

```bash
# Install useful development tools
npm install -D @types/react @types/react-dom eslint prettier
```

### 4. Project Structure

```
my-reflex-complement/
├── public/
│   └── vite.svg
├── src/
│   ├── components/
│   ├── assets/
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── package.json
├── vite.config.js
└── index.html
```

### 5. Basic Vite Configuration

Update `vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        host: true
    },
    build: {
        outDir: 'dist',
        sourcemap: true
    }
})
```

### 6. Run Development Server

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### 7. Integration with Reflex

Create a service file `src/services/reflexApi.js`:

```javascript
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000' // Adjust to your Reflex server

export const reflexApi = {
    // Add your Reflex API integration methods here
    getData: () => axios.get(`${API_BASE_URL}/api/data`),
    postData: (data) => axios.post(`${API_BASE_URL}/api/data`, data)
}
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint (if configured)

## Next Steps

1. Configure your Reflex backend API endpoints
2. Set up routing with React Router
3. Implement your complement components
4. Configure build settings for production deployment
