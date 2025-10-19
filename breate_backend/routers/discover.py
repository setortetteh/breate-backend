from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from breate_backend.database import get_db
from breate_backend import models

# ✅ Keep prefix consistent with main.py
router = APIRouter(prefix="/api/v1/discover", tags=["Discover"])

@router.get("/")
def discover_creators(
    name: str | None = Query(None),
    archetype_id: int | None = Query(None),
    tier_id: int | None = Query(None),
    db: Session = Depends(get_db)
):
    """
    Returns a filtered list of users based on name, archetype, and tier.
    """
    query = db.query(models.User)

    if name:
        query = query.filter(models.User.username.ilike(f"%{name}%"))
    if archetype_id:
        query = query.filter(models.User.archetype_id == archetype_id)
    if tier_id:
        query = query.filter(models.User.tier_id == tier_id)

    users = query.all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "bio": u.bio,
            "archetype": u.archetype.name if u.archetype else None,
            "tier": u.tier.name if u.tier else None,
        }
        for u in users
    ]
