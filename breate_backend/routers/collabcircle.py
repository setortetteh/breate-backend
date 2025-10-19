from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

# ✅ Correct absolute imports
from breate_backend import models, schemas
from breate_backend.database import get_db

router = APIRouter(prefix="/collabcircle", tags=["Collab Circle"])


# -----------------------------
# 1️⃣ Create a collaboration link (pending)
# -----------------------------
@router.post("/create")
def create_collab_link(link: schemas.CollabCreate, db: Session = Depends(get_db)):
    """
    Creates a pending collaboration link between two users (by username).
    Example body:
    {
        "user_a_username": "ama",
        "user_b_username": "kwame",
        "project_name": "Music Video"
    }
    """

    # Verify both users exist
    user_a = db.query(models.User).filter(models.User.username == link.user_a_username).first()
    user_b = db.query(models.User).filter(models.User.username == link.user_b_username).first()

    if not user_a or not user_b:
        raise HTTPException(status_code=404, detail="One or both users not found")

    # Prevent duplicate links
    existing = db.query(models.CollabLink).filter(
        ((models.CollabLink.user_a_username == link.user_a_username) &
         (models.CollabLink.user_b_username == link.user_b_username)) |
        ((models.CollabLink.user_a_username == link.user_b_username) &
         (models.CollabLink.user_b_username == link.user_a_username))
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Collaboration already exists")

    new_link = models.CollabLink(
        user_a_username=link.user_a_username,
        user_b_username=link.user_b_username,
        project_name=link.project_name,
        status="pending"
    )

    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return {"message": "Collaboration link created successfully.", "link_id": str(new_link.id)}


# -----------------------------
# 2️⃣ Verify collaboration (mutual confirmation)
# -----------------------------
@router.post("/verify")
def verify_link(user_a_username: str, user_b_username: str, db: Session = Depends(get_db)):
    """
    Marks a collaboration as verified using both usernames.
    """
    link = db.query(models.CollabLink).filter(
        ((models.CollabLink.user_a_username == user_a_username) &
         (models.CollabLink.user_b_username == user_b_username)) |
        ((models.CollabLink.user_a_username == user_b_username) &
         (models.CollabLink.user_b_username == user_a_username))
    ).first()

    if not link:
        raise HTTPException(status_code=404, detail="Collaboration not found")

    link.status = "verified"
    link.verified_at = datetime.utcnow()
    db.commit()

    return {"message": "Collaboration verified successfully."}


# -----------------------------
# 3️⃣ Fetch a user’s Collab Circle
# -----------------------------
@router.get("/{username}")
def get_collab_circle(username: str, db: Session = Depends(get_db)):
    """
    Returns all collaborations (pending + verified) for a specific user by username.
    """
    links = db.query(models.CollabLink).filter(
        (models.CollabLink.user_a_username == username) |
        (models.CollabLink.user_b_username == username)
    ).all()

    collab_circle = []
    for link in links:
        collaborator_username = (
            link.user_b_username if link.user_a_username == username else link.user_a_username
        )
        collab_circle.append({
            "collaborator_username": collaborator_username,
            "project_name": link.project_name,
            "status": link.status,
            "verified_at": getattr(link, "verified_at", None)
        })

    return {"collab_circle": collab_circle}
