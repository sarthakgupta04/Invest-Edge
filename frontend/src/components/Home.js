import React from 'react';
import { Typography, Container } from '@mui/material';

function Home() {
  return (
    <Container maxWidth="sm">
      <Typography variant="h2" gutterBottom>Welcome</Typography>
      <Typography variant="body1">Welcome to InvestEdge, your go-to platform for stock analysis and insights.</Typography>
    </Container>
  );
}

export default Home;
