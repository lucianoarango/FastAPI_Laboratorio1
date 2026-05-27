from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import engine
from .database import Base
from .database import get_db
from .controllers import persona_controller
from .error_handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(title="FastAPI Persona CRUD (MySQL)", version="1.0.0")

    # Register global exception handlers (domain → HTTP)
    register_exception_handlers(app)

    @app.on_event("startup")
    def on_startup() -> None:
        # Create tables at startup (demo purpose)
        Base.metadata.create_all(bind=engine)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    app.include_router(persona_controller.router)
    return app


app = create_app()

from sqlalchemy import text 

@app.get("/personas/estadisticas/dominios", tags=["Analítica Iván"])
def obtener_estadisticas_dominios(db: Session = Depends(get_db)):
    """
    Retorna la cantidad de personas registradas agrupadas por el dominio de su correo electrónico.
    """
    # 1. Consulta SQL para cortar el correo desde el '@' y contar
    query_sql = text("""
        SELECT 
            SUBSTRING_INDEX(email, '@', -1) AS dominio,
            COUNT(*) AS cantidad
        FROM personas
        WHERE email IS NOT NULL AND email LIKE '%@%'
        GROUP BY dominio
        ORDER BY cantidad DESC;
    """)

    try:
        # 2. Ejecutamos la consulta en MySQL
        resultado = db.execute(query_sql).fetchall()
        
        # 3. Formateamos la respuesta al JSON exacto que pide el PDF
        respuesta_json = {}
        for fila in resultado:
            dominio = fila[0]  # Ej: 'gmail.com'
            cantidad = fila[1] # Ej: 150
            respuesta_json[dominio] = cantidad
            
        return respuesta_json

    except Exception as e:

        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
@app.get("/personas/estadisticas/edad", tags=["Analítica Iván"])
def obtener_estadisticas_edad(db: Session = Depends(get_db)):
    """
    Calcula y retorna la edad promedio, mínima y máxima de todas las personas registradas.
    """
    # 1. Consulta SQL usando TIMESTAMPDIFF para calcular la edad exacta
    query_sql = text("""
        SELECT 
            ROUND(AVG(TIMESTAMPDIFF(YEAR, birth_date, CURDATE()))) AS edad_promedio,
            MIN(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_minima,
            MAX(TIMESTAMPDIFF(YEAR, birth_date, CURDATE())) AS edad_maxima
        FROM personas
        WHERE birth_date IS NOT NULL;
    """)

    try:
        # 2. Ejecutamos la consulta. Usamos fetchone() porque solo devuelve 1 fila con los 3 totales.
        resultado = db.execute(query_sql).fetchone()
        
        # 3. Validación: Si la tabla está vacía, SQL devuelve NULL. Lo manejamos aquí.
        if resultado[0] is None:
            return {
                "edad_promedio": 0,
                "edad_minima": 0,
                "edad_maxima": 0,
                "mensaje": "No hay datos suficientes."
            }

        # 4. Formateamos la respuesta al JSON exacto que pide el PDF
        respuesta_json = {
            "edad_promedio": int(resultado[0]),
            "edad_minima": int(resultado[1]),
            "edad_maxima": int(resultado[2])
        }
            
        return respuesta_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")   
@app.get("/personas/cumpleanios/mes/{numero_mes}", tags=["Analítica Iván"])
def obtener_cumpleanos_mes(numero_mes: str, db: Session = Depends(get_db)):
    """
    Retorna el listado de personas que cumplen años en un mes específico.
    Incluye validación estricta del parámetro de entrada (HTTP 400).
    """
    # 1. VALIDACIÓN DEFENSIVA (El Escudo)
    # Intentamos convertir lo que el usuario escribió en la URL a un número entero.
    try:
        mes_entero = int(numero_mes)
        if mes_entero < 1 or mes_entero > 12:
            raise ValueError() # Forzamos el error si pone un 13 o un 0
    except ValueError:
        # Si puso letras (ej. 'abc') o números fuera de rango, lanzamos el Error 400 exacto del PDF.
        raise HTTPException(
            status_code=400, 
            detail="El mes debe ser un entero entre 1 y 12."
        )

    # 2. CONSULTA SQL PARAMETRIZADA
    # Usamos :mes para inyectar el número de forma segura y evitar hackeos (SQL Injection).
    query_sql = text("""
        SELECT 
            id, first_name, last_name, email, phone, birth_date, is_active, notes
        FROM personas
        WHERE MONTH(birth_date) = :mes;
    """)

    try:
        # 3. Ejecutamos la consulta pasándole el mes validado
        resultado = db.execute(query_sql, {"mes": mes_entero}).fetchall()
        
        # 4. Formateamos la respuesta a una lista de diccionarios
        lista_cumpleaneros = []
        for fila in resultado:
            persona = {
                "id": fila[0],
                "first_name": fila[1],
                "last_name": fila[2],
                "email": fila[3],
                "phone": fila[4],
                "birth_date": str(fila[5]) if fila[5] else None, # Convertimos fecha a texto
                "is_active": bool(fila[6]), # Convertimos 1/0 a True/False
                "notes": fila[7]
            }
            lista_cumpleaneros.append(persona)
            
        return lista_cumpleaneros

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")