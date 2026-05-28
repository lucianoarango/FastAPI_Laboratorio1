# FastAPI Persona CRUD: LABORATORIO 1

Proyecto de insersión y consultas con endpoints, usando debidamente FastAPI + SQLAlchemy y estructura MVC para un CRUD de `Persona`. Dicho proyecto usa MySQL por defecto y permite apuntar a otra base SQL mediante la variable de entorno `DATABASE_URL` (configurable en `.env`).

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

## 3. Ejecutar el servidor o encender la API:
   ```bash
   uvicorn app.main:app --reload
   ```

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

# Endpoints Implementados — Marco Peñate

Durante el desarrollo del laboratorio se implementaron nuevos endpoints analíticos y operacionales sobre el modelo `Persona`, manteniendo la arquitectura MVC propuesta inicialmente en el proyecto.

Los endpoints desarrollados fueron implementados siguiendo la separación de responsabilidades entre:

* Controllers (manejo de rutas HTTP)
* Services (lógica de negocio)
* Views/Schemas (validación y serialización)
* Models (estructura de base de datos)

Además, todas las pruebas fueron verificadas mediante:

* Swagger UI
* Postman
* Base de datos MySQL (DBeaver)

---

# Endpoint E — Buscador General

## Descripción

Permite realizar búsquedas dinámicas sobre los campos:

* `first_name`
* `last_name`
* `email`

La búsqueda utiliza:

* operador SQL `OR`
* coincidencias parciales (`ILIKE`)
* búsqueda case-insensitive

## Ruta

```http
GET /personas/buscar/{termino}
```

## Ejemplo

```bash
curl -X GET "http://127.0.0.1:8000/personas/buscar/lopez"
```

## Respuesta esperada

```json
[
  {
    "id": 1,
    "first_name": "Maria",
    "last_name": "Lopez",
    "email": "maria@gmail.com",
    "phone": "+57 3001112233",
    "birth_date": "1998-05-10",
    "is_active": true,
    "notes": "Cliente frecuente",
    "created_at": "2026-05-27T03:40:17.292Z"
  }
]
```

---

# Endpoint F — Reporte de Activos

## Descripción

Retorna únicamente usuarios activos (`is_active = true`) usando una proyección reducida para optimizar la respuesta.
## Endpoints principales

- `GET /health` → estado del servicio
- `POST /personas` → crear persona
- `GET /personas` → listar personas (`skip`, `limit`)
- `GET /personas/{id}` → obtener persona por ID
- `PUT /personas/{id}` → actualizar (parcial) persona
- `DELETE /personas/{id}` → eliminar persona
- `POST /personas/poblar` → crear personas masivamente con Faker
- `DELETE /personas/reset` → eliminar todos los registros de personas
- `GET /personas/exportar/csv` → descargar todos los registros en CSV

### Esquemas (JSON)

- Crear:
  ```json
  {
    "first_name": "Juan",
    "last_name": "Pérez",
    "email": "juan.perez@example.com",
    "phone": "+57 3000000000",
    "birth_date": "1990-05-20",
    "is_active": true,
    "notes": "Cliente frecuente"
  }
  ```

- Actualizar (parcial):
  ```json
  {
    "email": "juan.perez2@example.com",
    "notes": "Actualizado"
  }
  ```

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


## Endpoints desarrollados por Luciano 

- `POST /personas/poblar`: recibe `{"cantidad": 50}` y crea entre 1 y 1000 personas usando Faker. Los correos se generan con dominios reales como `gmail.com`, `outlook.com`, `hotmail.com` y `yahoo.com`.
- `DELETE /personas/reset`: elimina todos los registros de la tabla `personas` y retorna cuantas filas fueron borradas.
- `GET /personas/exportar/csv`: descarga `personas.csv` con los campos `id`, `first_name`, `last_name`, `email`, `phone`, `birth_date`, `is_active` y `notes`.

### Verificacion de CSV y reset

Antes de exportar el CSV debe existir información en la tabla. Entonces primero puedes poblar algunos datos: 

```bash
curl -s -X POST http://127.0.0.1:8000/personas/poblar \
  -H 'Content-Type: application/json' \
  -d '{"cantidad":10}'
```

Luego exporta el CSV: 

```bash 
curl -OJ http://127.0.0.1:8000/personas/exportar/csv
```

El archivo `personas.csv` debe incluir encabezados y registros:

```csv
id,first_name,last_name,email,phone,birth_date,is_active,notes
1,Maria,Lopez,maria.lopez@gmail.com,+57  300 123 4567,1990-05-20,True,Nota de ejemplo
```

Para comprobar que el reset reinicia los IDs: 

```bash 
curl -s -X DELETE http://127.0.0.1:8000/personas/reset

curl -s -X POST http://127.0.0.1:8000/personas/poblar \
  -H 'Content-Type: applicaction/json' \
  -d '{"cantidad":5}'

curl -s http://127.0.0.1:8000/personas
```

Despues del reset, la nueva carga debe iniciar nuevamente desde `id = 1`.

En Postman, recuerda que `GET /personas/exportar/csv` no necesita body en la petición. Para ver el archivo usa **Send and Download**, o revisa la respuesta descargada.


## Validación sugerida en DBeaver

```sql
-- Verificar carga masiva 
SELECT COUNT(*) FROM personas;


-- Revisar que los dominios generados sean reales
SELECT SUBSTRING_INDEX(email, '@', -1) AS dominio, COUNT(*) AS total
FROM personas
GROUP BY dominio;


-- Verificar reset
SELECT COUNT(*) FROM personas;
```

## Detener el servidor

Campos expuestos:

* `id`
* `email`
* `phone`
* `is_active`

## Ruta

```http
GET /personas/reporte/activos
```

## Ejemplo

```bash
curl -X GET "http://127.0.0.1:8000/personas/reporte/activos"
```

## Respuesta esperada

```json
[
  {
    "id": 1,
    "email": "maria@gmail.com",
    "phone": "+57 3001112233",
    "is_active": true
  }
]
```

---

# Endpoint H — Desactivación Masiva

## Descripción

Permite desactivar múltiples usuarios en una sola operación mediante una lista de IDs.

El endpoint:

* desactiva únicamente IDs existentes
* ignora IDs inexistentes sin detener la operación
* reporta qué registros no fueron encontrados

## Validaciones implementadas

* La lista no puede estar vacía
* Máximo 100 IDs por solicitud
* Respuesta HTTP 400 en validaciones inválidas

## Ruta

```http
PATCH /personas/bulk/desactivar
```

## Request Body

```json
{
  "ids": [1, 2, 5, 999]
}
```

## Ejemplo

```bash
curl -X PATCH "http://127.0.0.1:8000/personas/bulk/desactivar" \
-H "Content-Type: application/json" \
-d '{
  "ids": [1,2,5,999]
}'
```

## Respuesta esperada

```json
{
  "message": "Operación completada.",
  "desactivados": [1,2,5],
  "no_encontrados": [999],
  "total_desactivados": 3
}
```

---

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

# Validaciones Aplicadas

## Buscador General

* búsqueda parcial
* búsqueda en múltiples campos

## Reporte de Activos

* filtrado exclusivo de usuarios activos
* reducción de datos retornados

## Desactivación Masiva

* máximo 100 IDs
* validación de lista vacía
* manejo de IDs inexistentes
* actualización masiva de registros

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
