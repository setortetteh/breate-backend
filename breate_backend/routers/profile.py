from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from breate_backend.database import get_db
from breate_backend import models
from breate_backend.routers.auth import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/{username}")
def get_profile(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.__dict__

@router.put("/{username}")
def update_profile(
    username: str,
    data: dict,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this profile")

    # Update allowed fields
    for field in [
        "full_name",
        "username",
        "bio",
        "preferred_themes",
        "portfolio_links",
        "next_build",
        "affiliations",
    ]:
        if field in data:
            setattr(user, field, data[field])

    db.commit()
    db.refresh(user)
    return {"message": "Profile updated successfully"}


