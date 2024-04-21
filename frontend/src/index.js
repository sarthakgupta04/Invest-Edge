import React from 'react';
import { createRoot } from 'react-dom/client';  // Import createRoot
import './index.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';

// Find the root element to mount your React app
const rootElement = document.getElementById('root');
const root = createRoot(rootElement);  // Create a root

// Render your App component within the AuthProvider and React.StrictMode
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
