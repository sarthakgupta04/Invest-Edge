import React from 'react';
import { AppBar, Toolbar, Button, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

function Navbar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" style={{ flexGrow: 1 }}>
          InvestEdge
        </Typography>
        <Button color="inherit" component={RouterLink} to="/">Home</Button>
        <Button color="inherit" component={RouterLink} to="/login">Login</Button>
        <Button color="inherit" component={RouterLink} to="/register">Register</Button>
        <Button color="inherit" component={RouterLink} to="/dashboard">Dashboard</Button>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
