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
    except HTTPException as http_exc:
        # Si el error viene del servicio y ya es un HTTPException (como el 400), lo dejamos pasar intacto.
        raise http_exc
    except Exception as e:
        # Si es un error inesperado (ej. se cayó MySQL), lanzamos un 500.
        raise HTTPException(status_code=500, detail=f"Error en el servicio de cumpleaños: {str(e)}")

