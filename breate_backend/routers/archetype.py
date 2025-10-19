from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from breate_backend.database import get_db
from breate_backend import models, schemas

router = APIRouter(
    prefix="/archetypes",
    tags=["Archetypes"]
)

# -----------------------------
# Get All Archetypes
# -----------------------------
@router.get("/", response_model=list[schemas.ArchetypeResponse])
def get_archetypes(db: Session = Depends(get_db)):
    """
    Returns all available archetypes.
    """
    archetypes = db.query(models.Archetype).all()
    if not archetypes:
        raise HTTPException(status_code=404, detail="No archetypes found")
    return archetypes
