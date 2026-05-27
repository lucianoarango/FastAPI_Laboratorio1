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
