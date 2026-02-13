# FastAPI Billing System

Este es un proyecto de ejemplo desarrollado con **FastAPI** y **SQLModel** para gestionar clientes, transacciones, facturas y planes.

## Requisitos Previos

- Python 3.10 o superior.
- Git (opcional).

## Instalación

Sigue estos pasos para configurar el proyecto localmente:

1. **Clonar el repositorio o navegar a la carpeta del proyecto:**
   ```bash
   cd fastapi
   ```

2. **Crear un entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual:**
   - En **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - En **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

## Cómo Correr la Aplicación

Para iniciar el servidor de desarrollo, ejecuta el siguiente comando:

```bash
fastapi dev app/main.py
```

La aplicación estará disponible en [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Documentación Interactiva

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

> **Nota**: El endpoint raíz (`/`) requiere autenticación básica:
> - **Usuario**: `admin`
> - **Contraseña**: `admin`

## Pruebas (Tests)

Para ejecutar los tests con Pytest:

```bash
pytest
```

## Estructura del Proyecto

- `app/main.py`: Punto de entrada de la aplicación y configuración de rutas.
- `app/db.py`: Configuración de la base de datos (SQLite) y sesiones.
- `app/models.py`: Definición de los modelos de datos (SQLModel).
- `app/routers/`: Módulos con las rutas para clientes, transacciones, facturas y planes.
- `app/tests/`: Pruebas unitarias e integrales.