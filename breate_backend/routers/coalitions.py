from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from breate_backend import models, schemas
from breate_backend.database import get_db

router = APIRouter(prefix="/coalitions", tags=["Coalitions"])


# ------------------------------------------------------
# ✅ Get all coalitions (with optional search & region filters)
# ------------------------------------------------------
@router.get("/", response_model=List[schemas.CoalitionsOut])
def get_coalitions(
    search: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Coalition)

    if search:
        s = f"%{search.lower()}%"
        query = query.filter(
            (models.Coalition.name.ilike(s))
            | (models.Coalition.focus.ilike(s))
            | (models.Coalition.location.ilike(s))
        )

    if region and region != "All":
        query = query.filter(models.Coalition.location == region)

    return query.all()


# ------------------------------------------------------
# ✅ Get single coalition by ID
# ------------------------------------------------------
@router.get("/{coalition_id}", response_model=schemas.CoalitionsOut)
def get_coalition(coalition_id: int, db: Session = Depends(get_db)):
    coalition = db.query(models.Coalition).filter(models.Coalition.id == coalition_id).first()
    if not coalition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coalition not found")
    return coalition


# ------------------------------------------------------
# ✅ Create a coalition (no creator_id at all)
# ------------------------------------------------------
@router.post("/", response_model=schemas.CoalitionsOut, status_code=status.HTTP_201_CREATED)
def create_coalition(coalition: schemas.CoalitionCreate, db: Session = Depends(get_db)):
    try:
        new_coalition = models.Coalition(
            name=coalition.name,
            description=coalition.description,
            focus=coalition.focus,
            location=coalition.location,
        )
        db.add(new_coalition)
        db.commit()
        db.refresh(new_coalition)
        return new_coalition
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating coalition: {str(e)}")


# ------------------------------------------------------
# ✅ Join a coalition
# ------------------------------------------------------
@router.post("/{coalition_id}/join", response_model=schemas.CoalitionsOut)
def join_coalition(coalition_id: int, user_id: int, db: Session = Depends(get_db)):
    coalition = db.query(models.Coalition).filter(models.Coalition.id == coalition_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not coalition or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coalition or user not found")

    if user in coalition.members:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already a member")

    coalition.members.append(user)
    db.commit()
    db.refresh(coalition)
    return coalition


# ------------------------------------------------------
# ✅ Leave a coalition
# ------------------------------------------------------
@router.post("/{coalition_id}/leave", response_model=schemas.CoalitionsOut)
def leave_coalition(coalition_id: int, user_id: int, db: Session = Depends(get_db)):
    coalition = db.query(models.Coalition).filter(models.Coalition.id == coalition_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not coalition or not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coalition or user not found")

    if user not in coalition.members:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not a member of this coalition")

    coalition.members.remove(user)
    db.commit()
    db.refresh(coalition)
    return coalition


# ------------------------------------------------------
# ✅ List coalition members
# ------------------------------------------------------
@router.get("/{coalition_id}/members", response_model=List[schemas.UserResponse])
def list_coalition_members(coalition_id: int, db: Session = Depends(get_db)):
    coalition = db.query(models.Coalition).filter(models.Coalition.id == coalition_id).first()
    if not coalition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coalition not found")
    return coalition.members


# ------------------------------------------------------
# ✅ Delete coalition (no creator check)
# ------------------------------------------------------
@router.delete("/{coalition_id}", status_code=status.HTTP_200_OK)
def delete_coalition(coalition_id: int, db: Session = Depends(get_db)):
    coalition = db.query(models.Coalition).filter(models.Coalition.id == coalition_id).first()
    if not coalition:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coalition not found")

    db.delete(coalition)
    db.commit()
    return {"detail": f"Coalition '{coalition.name}' deleted successfully"}












