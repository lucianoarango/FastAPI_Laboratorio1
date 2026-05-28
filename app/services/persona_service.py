from sqlalchemy import or_
from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.persona import Persona
from ..views.persona import PersonaCreate, PersonaUpdate
from .errors import PersonaNotFoundError, EmailAlreadyExistsError


def create_persona(db: Session, payload: PersonaCreate) -> Persona:
    """Create a Persona ensuring unique email."""
    # Optimistic check; DB unique constraint is the final guard
    if db.query(Persona).filter(Persona.email == payload.email).first():
        raise EmailAlreadyExistsError()
    obj = Persona(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        birth_date=payload.birth_date,
        is_active=payload.is_active,
        notes=payload.notes,
    )
    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        # Catch race conditions on unique email
        raise EmailAlreadyExistsError() from e
    db.refresh(obj)
    return obj


def list_personas(db: Session, skip: int = 0, limit: int = 100) -> Sequence[Persona]:
    """Return paginated list of Personas."""
    return db.query(Persona).offset(skip).limit(limit).all()


def get_persona(db: Session, persona_id: int) -> Persona:
    """Return Persona by ID or raise if not found."""
    obj = db.query(Persona).filter(Persona.id == persona_id).first()
    if not obj:
        raise PersonaNotFoundError()
    return obj


def update_persona(db: Session, persona_id: int, payload: PersonaUpdate) -> Persona:
    """Update Persona partially, enforcing unique email."""
    obj = db.query(Persona).filter(Persona.id == persona_id).first()
    if not obj:
        raise PersonaNotFoundError()

    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != obj.email:
        if db.query(Persona).filter(Persona.email == data["email"], Persona.id != persona_id).first():
            raise EmailAlreadyExistsError()

    for field, value in data.items():
        setattr(obj, field, value)

    db.add(obj)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise EmailAlreadyExistsError() from e
    db.refresh(obj)
    return obj


def delete_persona(db: Session, persona_id: int) -> None:
    """Delete Persona by ID or raise if not found."""
    obj = db.query(Persona).filter(Persona.id == persona_id).first()
    if not obj:
        raise PersonaNotFoundError()
    db.delete(obj)
    db.commit()

    
def search_personas(db: Session, termino: str):
    """
    Search personas by first name, last name or email.

    The search is case-insensitive and uses OR conditions,
    allowing the term to match any of the three fields.
    
    """

    # Search across multiple fields using OR
    return (
        db.query(Persona)
        .filter(
            or_(
                Persona.first_name.ilike(f"%{termino}%"),
                Persona.last_name.ilike(f"%{termino}%"),
                Persona.email.ilike(f"%{termino}%")
            )
        )
        .all()
    )


def get_active_personas_report(db: Session):
    """
    Return only active personas with reduced fields.

    This endpoint is used as a lightweight report,
    exposing only the required attributes.
    """

    return (
        db.query(Persona)
        .filter(Persona.is_active == True)
        .all()
    )


def bulk_deactivate_personas(db: Session, ids: list[int]):
    """
    Deactivate multiple personas in a single operation.

    The function:
    - Validates existing IDs
    - Deactivates only found personas
    - Reports missing IDs without failing
    """

    # Get all personas that exist in database
    personas = (
        db.query(Persona)
        .filter(Persona.id.in_(ids))
        .all()
    )

    # Extract IDs that actually exist
    found_ids = [persona.id for persona in personas]

    # Identify IDs that were not found
    not_found_ids = [
        persona_id for persona_id in ids
        if persona_id not in found_ids
    ]

    # Deactivate found personas
    for persona in personas:
        persona.is_active = False

    # Save changes in database
    db.commit()

    # Return response structure
    return {
        "message": "Operación completada.",
        "desactivados": found_ids,
        "no_encontrados": not_found_ids,
        "total_desactivados": len(found_ids)
    }