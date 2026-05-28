import csv
import random
import re
import unicodedata
from collections.abc import Iterator
from io import StringIO
from typing import Sequence

from faker import Faker
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models.persona import Persona
from ..views.persona import PersonaCreate, PersonaUpdate
from .errors import PersonaNotFoundError, EmailAlreadyExistsError

fake = Faker("es_CO")
REAL_EMAIL_DOMAINS = ("gmail.com", "outlook.com", "hotmail.com", "yahoo.com")
CSV_COLUMNS = ("id", "first_name", "last_name", "email", "phone", "birth_date", "is_active", "notes")



def _normalize_email_part(value: str) -> str:
    """Normalize names so Faker emails keep a clean nombre.apellido format."""
    without_accents = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "", without_accents.lower()) or "persona"


def _build_unique_email(first_name: str, last_name: str, used_emails: set[str]) -> str:
    """Build an email with a real domain and avoid collisions with existing records."""
    first = _normalize_email_part(first_name)
    last = _normalize_email_part(last_name)
    domain = random.choice(REAL_EMAIL_DOMAINS)


    #Try the requested nombre.apellido@dominio format first.
    email = f"{first}.{last}@{domain}"
    if email not in used_emails:
        used_emails.add(email)
        return email
    
    #If the same generated name already exists, add a shor numeric suffix.
    while True: 
        emial = f"{first}.{last}.{random.randint(1000, 9999)}@{domain}"
        if email not in used_emails:
            used_emails.add(email)
            return email
        

def _build_colombian_phone() -> str:
    """Return a realistic Colombian mobile phone number."""
    prefix = random.choice(("300", "301", "302", "310", "311", "312", "313", "314", "315", "316", "317", "310", "321"))
    return f"+57 {prefix} {random.randint(100,999)} {random.randint(1000,9999)}"


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
