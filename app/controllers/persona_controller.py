from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..views.persona import (
    PersonaCreate,
    PersonaUpdate,
    PersonaRead,
    PersonasPoblarRequest,
    PersonasPoblarResponse,
    PersonasResetResponse,
    PersonaActivaRead,
    BulkDeactivateRequest,
    BulkDeactivateResponse,
) 

# Import request and response schemas
from ..services import persona_service

router = APIRouter(prefix="/personas", tags=["personas"])


@router.post("", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    """Create a new Persona delegating to service layer."""
    # Let domain errors bubble up to global handlers
    return persona_service.create_persona(db, persona_in)


@router.get("", response_model=List[PersonaRead])
def list_personas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """List Personas with pagination via service layer."""
    return persona_service.list_personas(db, skip=skip, limit=limit)


@router.post("/poblar", response_model=PersonasPoblarResponse, status_code=status.HTTP_201_CREATED)
def poblar_personas(payload: PersonasPoblarRequest, db: Session = Depends(get_db)):
    """Create many 'Personas' using realistic Faker data."""
    if payload.cantidad <= 0 or payload.cantidad > 1000:
        raise HTTPException(status_code=400, detail="La cantidad debe ser un entero entre 1 y 1000.")
    
    created_count = persona_service.poblar_personas(db, payload.cantidad)
    return {
        "message": f"{created_count} usuarios creados exitosamente",
        "status": status.HTTP_201_CREATED,
    }


@router.delete("/reset", response_model=PersonasResetResponse, status_code=status.HTTP_200_OK)
def reset_personas(db: Session = Depends(get_db)):
    """Delete all 'Personas' so the lab can be restarted from a clean table."""
    deleted_count = persona_service.reset_personas(db)
    return {
        "message": "Base de datos limpiada. Se eliminaron todos los registros.",
        "deleted_count": deleted_count,
    }


@router.get("/exportar/csv")
def exportar_personas_csv(db: Session = Depends(get_db)):
    """Download every 'Persona' record as a CSV file for Excel, Pandas or terminal review."""
    csv_file = persona_service.build_personas_csv(db)
    headers = {"Content-Disposition": 'attachment; filename="personas.csv"'}
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers=headers,
    )


@router.get("/buscar/{termino}", response_model=List[PersonaRead])
def search_personas(termino: str, db: Session = Depends(get_db)):
    """
    Search personas by first name, last name or email.
    """
    
    # Delegate search logic to service layer
    return persona_service.search_personas(db, termino)


@router.get("/reporte/activos", response_model=List[PersonaActivaRead])
def get_active_personas_report(db: Session = Depends(get_db)):
    """
    Return a reduced report containing only active users.
    """

    # Delegate report logic to service layer
    return persona_service.get_active_personas_report(db)


@router.patch(
    "/bulk/desactivar",
    response_model=BulkDeactivateResponse
)
def bulk_deactivate_personas(
    payload: BulkDeactivateRequest,
    db: Session = Depends(get_db)
):
    """
    Deactivate multiple personas in a single request.
    """

    # Validation: list cannot be empty
    if not payload.ids:
        raise HTTPException(
            status_code=400,
            detail="The ids list cannot be empty."
        )

    # Validation: maximum 100 IDs allowed
    if len(payload.ids) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 IDs are allowed."
        )

    # Delegate business logic to service layer
    return persona_service.bulk_deactivate_personas(db, payload.ids)



@router.get("/{persona_id}", response_model=PersonaRead)
def get_persona(persona_id: int, db: Session = Depends(get_db)):
    """Retrieve a Persona by ID via service layer."""
    return persona_service.get_persona(db, persona_id)


@router.put("/{persona_id}", response_model=PersonaRead)
def update_persona(persona_id: int, persona_in: PersonaUpdate, db: Session = Depends(get_db)):
    """Update an existing Persona (partial) via service layer."""
    return persona_service.update_persona(db, persona_id, persona_in)


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Delete a Persona by ID via service layer."""
    persona_service.delete_persona(db, persona_id)
    return None
