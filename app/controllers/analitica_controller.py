from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.services import analitica_service

def obtener_estadisticas_dominios(db: Session):
    try:
        return analitica_service.obtener_estadisticas_dominios(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio de dominios: {str(e)}")

def obtener_estadisticas_edad(db: Session):
    try:
        return analitica_service.obtener_estadisticas_edad(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio de edad: {str(e)}")

def obtener_cumpleanos_mes(numero_mes: str, db: Session):
    try:
        return analitica_service.obtener_cumpleanos_mes(numero_mes, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el servicio de cumpleaños: {str(e)}")

