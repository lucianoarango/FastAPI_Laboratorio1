from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr


class PersonaBase(BaseModel):
    """Shared attributes for Persona inputs."""
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=30)
    birth_date: date | None = None
    is_active: bool = True
    notes: str | None = None


class PersonaCreate(PersonaBase):
    """Schema used for creating a new Persona."""
    pass


class PersonaUpdate(BaseModel):
    """Schema used for partial update of Persona."""
    first_name: str | None = Field(default=None, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    birth_date: date | None = None
    is_active: bool | None = None
    notes: str | None = None


class PersonaRead(BaseModel):
    """Schema used to return Persona data to clients."""
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    birth_date: date | None
    is_active: bool
    notes: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
    

class PersonasPoblarRequest(BaseModel):
    """Request body for creating many 'Personas' with Faker-generated data."""
    cantidad: int = Field(..., description="Number of 'personas' to generate. Valid Range: 1 to 1000.")


class PersonasPoblarResponse(BaseModel):
    """Response returned after the massive Faker load finishes."""
    message: str
    status: int


class PersonasResetResponse(BaseModel):
    """Response returned after deleting all 'personas' records."""
    message: str
    deleted_count: int


class PersonaActivaRead(BaseModel):
    """
    Schema used for active users report responses.
    Only exposes required fields for the report endpoint.
    """

    id: int
    email: EmailStr
    phone: str | None
    is_active: bool

    model_config = {"from_attributes": True}
    
    
class BulkDeactivateRequest(BaseModel):
    """
    Request schema for bulk deactivation endpoint.
    """

    ids: list[int]


class BulkDeactivateResponse(BaseModel):
    """
    Response schema for bulk deactivation operation.
    """

    message: str
    desactivados: list[int]
    no_encontrados: list[int]
    total_desactivados: int    


