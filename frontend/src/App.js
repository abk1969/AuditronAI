import React from 'react';
import { Container, Typography } from '@mui/material';

function App() {
  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h2" component="h1" gutterBottom>
        AuditronAI
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>
        Bienvenue sur votre plateforme d'audit de sécurité
      </Typography>
    </Container>
  );
}

export default App; 