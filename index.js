const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para leer JSON en las peticiones
app.use(express.json());

// Ruta de prueba
app.get('/', (req, res) => {
  res.json({ mensaje: 'API REST funcionando correctamente' });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});