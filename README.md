# APIs REST — Módulo de usuarios con registro, login y foto de perfil (Flask)

Este proyecto es un **módulo base reutilizable** para autenticación y gestión de usuarios en Flask.
Te sirve para arrancar rápido nuevos proyectos con:
- registro de usuarios,
- inicio de sesión con sesiones,
- perfil personal,
- subida de foto,
- y panel de administración oculto.

Está pensado para que lo puedas copiar/adaptar en otros repos y no empezar desde cero.

### ✨ Funcionalidades

- Registro público de usuarios en `/registro`.
- Registro con **foto de perfil opcional** (si no subes foto, el usuario se crea igual).
- Inicio de sesión con sesión Flask (`/api/login`).
- Página **Mi cuenta** (`/mi-cuenta`) para ver solo tus datos.
- Cambio de foto desde **Mi cuenta** (`/api/foto`).
- Panel de administración oculto (`/usuarios`) visible solo para emails definidos en `ADMIN_EMAILS`.
- API REST de usuarios con endpoints de lectura/edición/borrado protegidos para admin.
- Base de datos SQLite local por proyecto (`instance/usuarios.db`) no versionada.
- Carpeta de subidas local (`uploads/`) no versionada.
- Interfaz HTML/CSS con degradados y logo (`static/logoFB.png`).

### 🧰 Tecnologías

- **Python**
- **Flask**
- **Flask-SQLAlchemy**
- **SQLite**
- **HTML / CSS / JavaScript** (con `fetch` y `FormData`)
- **Git / GitHub**

### 📁 Estructura del proyecto

```text
src/
└── api/
    ├── app.py
    ├── routes.py
    ├── models.py
    ├── usuarios.html
    ├── page/
    │   ├── home.html
    │   ├── registro.html
    │   ├── ingresar.html
    │   └── mi-cuenta.html
    ├── static/
    │   └── logoFB.png
    ├── instance/
    │   └── usuarios.db
    └── uploads/
```

Explicación rápida:

- `src/api/app.py`: configuración principal de Flask (DB, sesiones, páginas, `/uploads/<path:nombre>`, rutas públicas/protegidas).
- `src/api/routes.py`: endpoints REST (`/api/...`), login, permisos admin, y subida de foto.
- `src/api/models.py`: modelo `User` de SQLAlchemy.
- `src/api/usuarios.html`: panel de usuarios registrados (solo admin).
- `src/api/page/home.html`: página de inicio pública (`/`).
- `src/api/page/registro.html`: registro público con vista previa de foto opcional.
- `src/api/page/ingresar.html`: formulario de login (redirige a `/mi-cuenta` al iniciar).
- `src/api/page/mi-cuenta.html`: datos del usuario logueado + cambio de foto + enlace admin condicional.
- `src/api/static/logoFB.png`: logo visual del proyecto.
- `src/api/instance/usuarios.db`: SQLite local del proyecto (ignorada por Git).
- `src/api/uploads/`: imágenes subidas por usuarios (ignorada por Git).

> Nota: `instance/` y `uploads/` están en `.gitignore`, por eso son locales.

### 🚀 Cómo ejecutarlo

1. Ir al proyecto:

```bash
cd /home/ubuntu/github_repos/APIs_REST
```

2. (Opcional pero recomendado) Crear entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

Si `requirements.txt` no tiene paquetes definidos, instala manualmente:

```bash
pip install flask flask-sqlalchemy
```

4. Ejecutar Flask:

```bash
cd src/api
python app.py
```

5. Abrir en el navegador:

```text
http://localhost:5000
```

### 🌐 Páginas y flujo

| Ruta | Acceso | Qué hace |
|---|---|---|
| `/` | Pública | Home con botones **Registrarse** e **Ingresar** |
| `/registro` | Pública | Crea usuarios (con foto opcional) |
| `/ingresar` | Pública | Login; si es correcto redirige a `/mi-cuenta` |
| `/mi-cuenta` | Requiere sesión | Muestra tus datos y permite cambiar tu foto |
| `/usuarios` | Solo admin (y sesión) | Lista de usuarios registrados |
| `/logout` | Requiere sesión activa para tener efecto | Cierra sesión y vuelve a `/` |

Flujo usuario normal:
1. Se registra en `/registro`.
2. Inicia sesión en `/ingresar`.
3. Entra a `/mi-cuenta`.
4. Si intenta abrir `/usuarios`, es redirigido a `/mi-cuenta`.
5. Si llama `/api/usuarios`, recibe `403`.

Flujo admin:
1. Inicia sesión con un email incluido en `ADMIN_EMAILS`.
2. En `/mi-cuenta` aparece el botón **Ver usuarios registrados**.
3. Puede abrir `/usuarios` y consultar `/api/usuarios`.

### 🔌 Endpoints de la API

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| GET | `/api/usuarios` | Admin | Lista todos los usuarios |
| GET | `/api/usuarios/<id>` | Admin | Devuelve un usuario por ID |
| POST | `/api/usuarios` | Público | Registro de usuario (acepta JSON o `FormData`; foto opcional) |
| PUT | `/api/usuarios/<id>` | Admin | Actualiza usuario |
| DELETE | `/api/usuarios/<id>` | Admin | Elimina usuario |
| POST | `/api/login` | Público | Inicia sesión y crea sesión Flask |
| GET | `/api/yo` | Sesión | Devuelve datos del usuario logueado + campo `admin` |
| POST | `/api/foto` | Sesión | Sube o reemplaza la foto del usuario logueado |

Ejemplos `curl`:

**1) Crear usuario con JSON (sin foto):**

```bash
curl -X POST http://localhost:5000/api/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana","email":"ana@test.com","password":"1234"}'
```

**2) Crear usuario con foto (`multipart/form-data`):**

```bash
curl -X POST http://localhost:5000/api/usuarios \
  -F "nombre=Fernando" \
  -F "email=fer@test.com" \
  -F "password=1234" \
  -F "foto=@/ruta/a/tu/imagen.png"
```

**3) Login guardando cookie de sesión:**

```bash
curl -c /tmp/cookies.txt -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"fer@test.com","password":"1234"}'
```

### 🖼️ Cómo funciona la foto de perfil

- Extensiones permitidas: `png`, `jpg`, `jpeg`, `gif`.
- Tamaño máximo de subida: **5 MB** (`MAX_CONTENT_LENGTH`).
- Al guardar, el archivo se nombra como:
  - `uploads/usuario_<id>_<archivo_original_seguro>`
- La columna `foto` del usuario guarda la ruta pública, por ejemplo:
  - `/uploads/usuario_1_mifoto.png`
- Flask sirve esas imágenes desde:
  - `/uploads/<nombre>`

### 🔐 Panel de administración

En `src/api/routes.py` está definido:

```python
ADMIN_EMAILS = {"ferbarotz23@gmail.com"}
```

Qué implica:
- Solo ese email (u otros que agregues ahí) puede ver `/usuarios` y usar endpoints admin de usuarios.
- Usuario normal:
  - si entra a `/usuarios` → redirección a `/mi-cuenta`.
  - si llama `/api/usuarios` (GET/PUT/DELETE por ID también) → respuesta `403`.

Importante de seguridad actual:
- La contraseña se guarda en texto plano en la base de datos (`password` sin hash).
- Es funcional para práctica, pero **no es seguro para producción**.

### ♻️ Cómo reutilizarlo en otro proyecto

Opción A (rápida): copiar la carpeta `src/api` a otro proyecto.

Opción B: clonar este repo y adaptarlo.

Pasos recomendados:

1. Copia el módulo (`src/api`) o clona el repositorio.
2. Cambia el logo en `src/api/static/logoFB.png`.
3. Ajusta textos/nombre visual de la app en los HTML de `src/api/page/` y `src/api/usuarios.html`.
4. Cambia `SECRET_KEY` en `src/api/app.py`.
5. Cambia `ADMIN_EMAILS` en `src/api/routes.py`.
6. Instala dependencias y ejecuta con `python app.py`.

Recordatorio clave:
- Cada copia usa su **propia base de datos local SQLite**.
- Los usuarios de un proyecto **no se comparten** automáticamente con otro.

### 📝 Historial de cambios

Commits principales (verificados en `git log --oneline`):

- `528bffb` — home con navbar y nuevas rutas base.
- `88a16e1` — separación de registro y lista de usuarios.
- `edc81cb` — se quitó enlace a lista desde mensaje de registro.
- `d12ad85` — login con sesión y protección inicial de lista.
- `55daf6c` — botón salir que cierra sesión.
- `9e53534` — cabecera APIs + espacio de foto + botón cambiar foto.
- `9c1bb7d` — `.gitignore` para no versionar SQLite/cache/subidas.
- `59a9e43` — logo y título APIs fuera del cuadro en `/usuarios`.
- `19cb016` — subida y muestra de foto de perfil (`/api/foto`, `/api/yo`, `/uploads/...`).
- `1c837f0` — foto opcional desde registro (`/api/usuarios` con JSON/FormData).
- `f26cac7` — página Mi cuenta y panel de usuarios solo admin.

### ⚠️ Pendientes / ideas futuras

- Cifrar contraseñas con hash:
  - `generate_password_hash` / `check_password_hash` de `werkzeug.security`.
- Validar el tipo real del archivo de imagen (no solo extensión).
- Definir foto por defecto para usuarios sin imagen.
- Confirmación de email en registro.
- Recuperación de contraseña.
- Separar configuración por entorno (desarrollo/producción).
- Mejorar control de errores y logs.

---

Proyecto de práctica de Fernando Barrera Ortiz (@Ferbarotz)
