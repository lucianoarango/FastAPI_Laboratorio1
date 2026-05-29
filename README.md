# FastAPI Persona CRUD: LABORATORIO 1

Proyecto de insersión y consultas con endpoints, usando debidamente FastAPI + SQLAlchemy y estructura MVC para un CRUD de `Persona`. Dicho proyecto usa MySQL por defecto y permite apuntar a otra base SQL mediante la variable de entorno `DATABASE_URL` (configurable en `.env`).

El proyecto conserva los endpoints originales del CRUD y agrega los 9 endpoints solicitados en el laboratorio.

# Requisitos/ Herramientas de trabajo

- Python 3.10+ (recomendado 3.12)
- FastAPI
- SQLAlchemy
- MySQL
- PyMySQL
- Postman
- DBeaver

---

# Instalación y ejecución

## 1. Crear entorno virtual e instalar dependencias:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate # macOS / Linux
   .venv\Scripts\activate # Windows
   pip install -r requirements.txt
   ```

## 2. Configurar variables de entorno:
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales de MySQL
   # Normalmente están configuradas así: DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fastapi_demo
   ```

## 3. Crear/verificar la base de datos:
   ```bash
   python scripts/init_db.py
   ```

## 4. Ejecutar el servidor o encender la API:
   ```bash
   uvicorn app.main:app --reload
   ```

## 6. Abrir Swagger:
Estos endpoints se pueden probar facilmente desde Swagger:

   ```text
   http://127.0.0.1:8000/docs#/
   ```

En Swagger puedes buscar:

- `GET /personas/estadisticas/dominios`
- `GET /personas/estadisticas/edad`
- `GET /personas/cumpleanios/mes/{numero_mes}`


## Conexión a otras bases de datos

Edita `DATABASE_URL` en el archivo `.env`.
- MySQL: `mysql+pymysql://user:password@localhost:3306/mydb` 

## Ejemplo de `.env` (MySQL local)

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/nombre_basedatos

```
# Arquitectura MVC

| Directorio | Componente MVC | Tecnología | Descripción |
| :--- | :--- | :--- | :--- |
| `app/models/` | **Modelo** | SQLAlchemy | Modelos de la base de datos y mapeo ORM. |
| `app/views/` | **Vista** | Pydantic | Esquemas de datos, serialización y validaciones. |
| `app/controllers/` | **Controlador** | FastAPI | Rutas, endpoints y gestión de peticiones. |
| `app/services/` | **Lógica** | Python Puro | Servicios y reglas de negocio del sistema. |



#  ENDPOINTS PRINCIPALES TRABAJADOS EN ESTE PROYECTO.

## Endpoints desarrollados por integrante

El laboratorio fue dividido por integrante para implementar los 9 nuevos endpoints solicitados, manteniendo intactos los endpoints originales del CRUD.

### Luciano Arango - Operaciones masivas y exportacion

Luciano desarrollo los endpoints relacionados con carga masiva de datos, limpieza de la tabla y exportacion de informacion.

- `POST /personas/poblar`: crea una cantidad determinada de personas usando Faker. Genera nombres, apellidos, correos con dominios reales, telefonos, fechas de nacimiento, estado activo/inactivo y notas.
- `DELETE /personas/reset`: elimina todos los registros de la tabla `personas` y reinicia el contador de IDs para que una nueva carga empiece desde `id = 1`.
- `GET /personas/exportar/csv`: exporta todos los registros de la tabla en formato CSV descargable, incluyendo `id`, `first_name`, `last_name`, `email`, `phone`, `birth_date`, `is_active` y `notes`.

### Ivan - Analitica y filtros por fecha

Ivan desarrollo los endpoints de analitica sobre los datos registrados y el filtro de cumpleanios por mes.

- `GET /personas/estadisticas/dominios`: agrupa las personas por dominio de correo y retorna la cantidad registrada por cada proveedor, por ejemplo `gmail.com`, `outlook.com` o `hotmail.com`.
- `GET /personas/estadisticas/edad`: calcula estadisticas de edad usando el campo `birth_date`, retornando edad promedio, edad minima y edad maxima.
- `GET /personas/cumpleanios/mes/{numero_mes}`: retorna las personas que cumplen anios en el mes indicado. El parametro `numero_mes` debe estar entre `1` y `12`; si no cumple la validacion, retorna `400 Bad Request`.

Estos endpoints se pueden probar facilmente desde Swagger:

```text
http://127.0.0.1:8000/docs#/
```

En Swagger puedes buscar:

- `GET /personas/estadisticas/dominios`
- `GET /personas/estadisticas/edad`
- `GET /personas/cumpleanios/mes/{numero_mes}`

### Marco Penate - Busqueda, reportes y desactivacion masiva

Marco desarrollo los endpoints de busqueda general, reporte de usuarios activos y desactivacion masiva.

- `GET /personas/buscar/{termino}`: busca el termino recibido en los campos `first_name`, `last_name` o `email`, retornando todas las coincidencias encontradas.
- `GET /personas/reporte/activos`: retorna un reporte reducido solo con las personas activas, mostrando unicamente `id`, `email`, `phone` e `is_active`.
- `PATCH /personas/bulk/desactivar`: recibe una lista de IDs y desactiva las personas existentes, marcando `is_active = false`. Si algunos IDs no existen, no falla la operacion y los reporta en `no_encontrados`.

## Resumen de responsabilidades

| Integrante | Endpoints desarrollados |
| --- | --- |
| Luciano Arango | `POST /personas/poblar`, `DELETE /personas/reset`, `GET /personas/exportar/csv` |
| Ivan | `GET /personas/estadisticas/dominios`, `GET /personas/estadisticas/edad`, `GET /personas/cumpleanios/mes/{numero_mes}` |
| Marco Penate | `GET /personas/buscar/{termino}`, `GET /personas/reporte/activos`, `PATCH /personas/bulk/desactivar` |


## Colección de Postman

Importa `FastAPI-CRUD-Demo.postman_collection.json` en Postman. Variables:

- `base_url` (por defecto `http://localhost:8000`)
- `persona_id` (por defecto `1`)

## Notas

- Las tablas se crean automáticamente al iniciar (solo con fines de demo).
- Asegúrate de crear la base de datos en MySQL y de que el usuario tenga permisos (por ejemplo, `CREATE DATABASE fastapi_demo;`).

## Estructura MVC

- `app/models/` → modelos SQLAlchemy (por ejemplo, `persona.py`).
- `app/views/` → esquemas Pydantic (por ejemplo, `persona.py`).
- `app/controllers/` → routers/controladores FastAPI (por ejemplo, `persona_controller.py`).

## Pruebas rápidas (curl)

```bash
# Health

curl -s http://127.0.0.1:8000/health

# Crear persona

curl -s -X POST http://127.0.0.1:8000/personas \
  -H 'Content-Type: application/json' \
  -d '{
    "first_name":"Juan",
    "last_name":"Perez",
    "email":"juan.perez@example.com",
    "phone":"+57 3000000000",
    "birth_date":"1990-05-20",
    "is_active":true,
    "notes":"Cliente frecuente"
  }'

# Listar

curl -s http://127.0.0.1:8000/personas

# Obtener por ID

curl -s http://127.0.0.1:8000/personas/1

# Actualizar parcial

curl -s -X PUT http://127.0.0.1:8000/personas/1 \
  -H 'Content-Type: application/json' \
  -d '{"email":"juan.perez2@example.com","notes":"Actualizado"}'

# Eliminar

curl -s -X DELETE http://127.0.0.1:8000/personas/1 -i

# Poblar 50 personas con Faker

curl -s -X POST http://127.0.0.1:8000/personas/poblar \
  -H 'Content-Type: application/json' \
  -d '{"cantidad":50}'


# Descargar CSV

curl -s -OJ http://127.0.0.1:8000/personas/exportar/csv


# Resetear tabla de personas

curl -s -X DELETE http://127.0.0.1:8000/personas/reset
```


## Detener el servidor

Campos expuestos:

* `id`
* `email`
* `phone`
* `is_active`


# Tecnologías Utilizadas

* FastAPI
* SQLAlchemy
* Pydantic
* MySQL
* PyMySQL
* Swagger UI
* Postman
* DBeaver
* Python 3.11


---

# Evidencias y pruebas

Todos los endpoints fueron:

* ejecutados correctamente desde Swagger UI
* probados en Postman
* verificados directamente en MySQL usando DBeaver

Los códigos HTTP esperados fueron validados:

* `200 OK`
* `201 Created`
* `400 Bad Request`

