const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware para leer JSON en las peticiones
app.use(express.json());

// Datos en memoria (demo del servidor Express).
// El proyecto principal Flask vive en src/api/ con SQLite.
const usuarios = [
  { id: 1, nombre: 'Fernando', email: 'ferbarotz23@gmail.com' },
];

// Ruta de prueba
app.get('/', (req, res) => {
  res.json({ mensaje: 'API REST funcionando correctamente' });
});

// API: datos en JSON que consume la página
app.get('/api/usuarios', (req, res) => {
  res.json(usuarios);
});

// Sirve la página html de usuarios si existe, si no responde JSON
app.get('/usuarios', (req, res) => {
  const rutaHtml = path.join(__dirname, 'src', 'api', 'usuarios.html');
  res.sendFile(rutaHtml, (err) => {
    if (err) {
      res.status(404).json({ error: 'Página de usuarios no encontrada' });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Servidor escuchando en http://localhost:${PORT}`);
});
