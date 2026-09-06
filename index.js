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

// Sirve la página html de usuarios
app.get('/usuarios', (req, res) => {
  res.sendFile(__dirname + '/usuarios.html');
});

// API: datos en JSON que consume la página
app.get('/api/usuarios', (req, res) => {
  res.json(usuarios);
});