import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, TextField, Button, Typography, Alert, CircularProgress } from '@mui/material';
import axios from 'axios';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');  // State to hold error message
  const [loading, setLoading] = useState(false);  // State to handle loading state
  const navigate = useNavigate();

  const handleLogin = async () => {
    setError('');  // Clear previous errors
    setLoading(true);  // Start loading
    try {
      const response = await axios.post('http://127.0.0.1:5000/app/auth/login', {
        username,
        password
      });
      console.log('Login successful:', response.data);
      navigate('/dashboard'); // Redirect to dashboard after login
    } catch (error) {
      console.error('Login error:', error);
      if (error.response) {
        // Handle HTTP errors
        console.error('Error data:', error.response.data);
        setError('Login failed: ' + (error.response.data.message || 'Invalid credentials'));
      } else if (error.request) {
        // The request was made but no response was received
        console.error('Error request:', error.request);
        setError('Login failed: Server did not respond.');
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error message:', error.message);
        setError('Login failed: ' + error.message);
      }
    } finally {
      setLoading(false);  // End loading
    }
  };

  return (
    <Container maxWidth="xs">
      <Typography variant="h4" gutterBottom>Login</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      <TextField
        label="Username"
        fullWidth
        margin="normal"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        autoComplete="username"
      />
      <TextField
        label="Password"
        fullWidth
        type="password"
        margin="normal"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        autoComplete="current-password"
      />
      <Button 
        variant="contained" 
        color="primary" 
        fullWidth 
        onClick={handleLogin}
        disabled={loading}  // Disable button when loading
      >
        {loading ? <CircularProgress size={24} /> : 'Login'}
      </Button>
    </Container>
  );
}

export default Login;
