# Práctica 5 — XSS (Cross-Site Scripting)
### Seguridad Informática — UPQ — Grupo S-203
### Alumno: Jesús (ID 123048152)

Laboratorio práctico de Cross-Site Scripting implementado en Flask, con
estructura estándar de proyecto (rutas, templates Jinja2, CSS/JS estáticos)
y persistencia real en **PostgreSQL** para la demostración de XSS Almacenado.

---

## 📁 Estructura del proyecto

```
proyecto_final/
│
├── app.py                  # Aplicación Flask — rutas y lógica
├── db.py                    # Modelo y conexión a PostgreSQL (SQLAlchemy)
├── requirements.txt         # Dependencias del proyecto
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos ignorados por git
├── README.md                # Este archivo
│
├── templates/                # Plantillas Jinja2 (HTML)
│   ├── base.html             # Layout base con nav y estilos comunes
│   ├── vulnerable.html       # XSS Reflejado — vulnerable
│   ├── seguro.html           # XSS Reflejado — mitigado
│   ├── almacenado.html       # XSS Almacenado — vulnerable (PostgreSQL)
│   ├── dom.html               # XSS basado en DOM — vulnerable
│   └── info.html             # Tabla de payloads y mitigaciones
│
├── static/
│   ├── css/
│   │   └── style.css         # Hoja de estilos de toda la app
│   └── js/
│       └── dom_vuln.js       # Script vulnerable a XSS DOM
│
└── docs/
    ├── Practica5_XSS_Jesus_S203.docx   # Reporte académico (formato UPQ)
    └── init_db.sql                       # Script SQL opcional de creación manual
```

---

## 🐘 Configurar PostgreSQL

### 1. Instalar PostgreSQL (si no lo tienes)
Descarga el instalador desde https://www.postgresql.org/download/windows/
Durante la instalación, recuerda la contraseña que le pongas al usuario `postgres`.

### 2. Crear la base de datos

Abre **pgAdmin** o la terminal `psql` y ejecuta:

```sql
CREATE DATABASE xss_lab;
```

> No necesitas crear la tabla manualmente — la aplicación la crea sola la
> primera vez que se ejecuta (ver `db.py`, función `init_db`). El archivo
> `docs/init_db.sql` queda como referencia opcional si prefieres crearla
> a mano desde pgAdmin.

### 3. Configurar las credenciales

```powershell
# Copia la plantilla y renómbrala
copy .env.example .env
```

Edita `.env` con tus datos reales:

```env
DB_USER=postgres
DB_PASSWORD=tu_password_real
DB_HOST=localhost
DB_PORT=5432
DB_NAME=xss_lab
```

---

## ⚙️ Instalación y ejecución

### Requisitos
- Python 3.8 o superior
- PostgreSQL instalado y corriendo
- pip

### Pasos

```powershell
# 1. Entrar a la carpeta del proyecto
cd proyecto_final

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Configurar .env (ver sección anterior)
copy .env.example .env

# 6. Ejecutar la aplicación
python app.py
```

Abre el navegador en: **http://127.0.0.1:5000**

Si la conexión a PostgreSQL es correcta, verás en la consola que Flask
arranca sin errores y la tabla `comentarios` se crea automáticamente.

---

## 🗺️ Rutas de la aplicación

| Ruta | Tipo | Descripción | Persistencia |
|------|------|-------------|---------------|
| `/` | — | Redirige a `/vulnerable` | — |
| `/vulnerable` | XSS Reflejado | Sin sanitización — el payload se ejecuta | No persiste (solo en la URL) |
| `/seguro` | Mitigado | Con escape(), CSP y headers de seguridad | No persiste |
| `/almacenado` | XSS Almacenado | Comentarios sin sanitizar — **se guardan en PostgreSQL** | **Sí — tabla `comentarios`** |
| `/dom` | XSS DOM | innerHTML + location.hash sin escape | No persiste (lado cliente) |
| `/info` | Referencia | Tabla de payloads y mitigaciones | — |

---

## 🧪 Paso a paso para la práctica

### PASO 1 — XSS Reflejado básico
1. Ve a `http://127.0.0.1:5000/vulnerable`
2. En el campo de búsqueda escribe:
   ```
   <script>alert('XSS Reflejado - Jesús S203')</script>
   ```
3. Presiona **Buscar** y toma captura del alert() ejecutado

### PASO 2 — Bypass con onerror (sin tag script)
1. En `/vulnerable`, escribe:
   ```
   <img src=x onerror="alert('Cookie: ' + document.cookie)">
   ```
2. Observa que se ejecuta aunque no uses `<script>` — toma captura

### PASO 3 — XSS Almacenado (persistido en PostgreSQL)
1. Ve a `http://127.0.0.1:5000/almacenado`
2. En "Comentario" escribe:
   ```
   <script>alert('Soy un XSS almacenado en PostgreSQL')</script>
   ```
3. Publica, recarga la página — el script se ejecuta de nuevo automáticamente
4. **Verifica la persistencia real**: cierra la app (Ctrl+C), vuelve a
   ejecutar `python app.py`, recarga `/almacenado` — el payload sigue ahí
   porque vive en la tabla `comentarios` de PostgreSQL
5. (Opcional) Abre pgAdmin y ejecuta `SELECT * FROM comentarios;` para
   ver el payload guardado tal cual en la base de datos — útil como
   captura adicional para el reporte
6. Toma capturas antes y después

### PASO 4 — XSS DOM
1. Ve directamente a:
   ```
   http://127.0.0.1:5000/dom#<img src=x onerror=alert('DOM XSS')>
   ```
2. El script se ejecuta sin que el servidor reciba el payload (va en el hash #)
3. Toma captura del alert y de DevTools → Network (verás que el servidor no lo recibió)

### PASO 5 — Verificar mitigación
1. Ve a `http://127.0.0.1:5000/seguro`
2. Repite el payload del Paso 1
3. Observa que se muestra como texto plano: `&lt;script&gt;alert('XSS')&lt;/script&gt;`
4. Abre DevTools → Network → Headers para confirmar el CSP activo
5. Toma capturas

---

## 📸 Checklist de capturas para el reporte

- [ ] Alert ejecutado en `/vulnerable` (Paso 1)
- [ ] Alert con onerror (Paso 2)
- [ ] Comentario malicioso publicado y persistente (Paso 3)
- [ ] Consulta `SELECT * FROM comentarios;` en pgAdmin mostrando el payload guardado (Paso 3, opcional)
- [ ] DOM XSS en URL con hash (Paso 4)
- [ ] Payload sanitizado en `/seguro` (Paso 5)
- [ ] Headers HTTP en DevTools (Paso 5)

---

## 🛡️ Resumen de mitigaciones implementadas

| Técnica | Dónde | Protege contra |
|---------|-------|-----------------|
| `markupsafe.escape()` | `/seguro` | XSS Reflejado y Almacenado |
| Content-Security-Policy | Header en `/seguro` | Scripts inline/externos |
| X-XSS-Protection | Header en `/seguro` | XSS detectado por navegador |
| `textContent` vs `innerHTML` | Comentado en `dom_vuln.js` | XSS basado en DOM |
| Queries parametrizadas (SQLAlchemy ORM) | `db.py` | SQL Injection (mencionado como referencia adicional) |

---

## ⚠️ Notas importantes

- Proyecto para uso **local únicamente**, con fines educativos
- El archivo `.env` con tus credenciales reales **nunca** se sube a git (ya está en `.gitignore`)
- La tabla `comentarios` SÍ persiste entre reinicios — a diferencia de la
  versión anterior con lista en memoria, ahora los datos viven en disco
- Para comparar vulnerable vs. seguro, abre ambas rutas en pestañas distintas con el mismo payload
- El reporte académico completo está en `docs/Practica5_XSS_Jesus_S203.docx`

---

## 🔧 Solución de problemas comunes

**Error: `could not connect to server`**
PostgreSQL no está corriendo. En Windows, revisa el servicio "postgresql-x64-..." en Servicios (services.msc) y arráncalo.

**Error: `password authentication failed`**
Revisa que `DB_PASSWORD` en tu `.env` coincida exactamente con la contraseña que pusiste al instalar PostgreSQL.

**Error: `database "xss_lab" does not exist`**
No ejecutaste el `CREATE DATABASE xss_lab;` del paso 2. Créala desde pgAdmin o psql antes de correr la app.

**Error: `ModuleNotFoundError: No module named 'psycopg2'`**
Te faltó instalar dependencias: `pip install -r requirements.txt` dentro del entorno virtual activado.
