from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import engine
from .database import Base
from .database import get_db
from .controllers import persona_controller
from .error_handlers import register_exception_handlers
from .controllers import analitica_controller

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
def estadisticas_dominios(db: Session = Depends(get_db)):
    return analitica_controller.obtener_estadisticas_dominios(db)

@app.get("/personas/estadisticas/edad", tags=["Analítica Iván"])
def estadisticas_edad(db: Session = Depends(get_db)):
    return analitica_controller.obtener_estadisticas_edad(db)

@app.get("/personas/cumpleanios/mes/{numero_mes}", tags=["Analítica Iván"])
def cumpleanos_mes(numero_mes: str, db: Session= Depends(get_db)):
    return analitica_controller.obtener_cumpleanos_mes(numero_mes, db)