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
