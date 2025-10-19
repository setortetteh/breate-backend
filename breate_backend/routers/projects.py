print("✅ Projects router loaded successfully!")

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from breate_backend.database import get_db
from breate_backend import models

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

# ---------------------------------------------------------
# ✅ Schemas
# ---------------------------------------------------------
class ProjectBase(BaseModel):
    title: str
    objective: str
    project_type: str
    needed_archetypes: List[str]
    open_roles: Optional[str] = None
    timeline: Optional[str] = None
    region: Optional[str] = None
    coalition_tags: Optional[List[str]] = []
    poster_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ---------------------------------------------------------
# ✅ GET all projects
# ---------------------------------------------------------
@router.get("/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).order_by(models.Project.created_at.desc()).all()
    return [
        ProjectResponse(
            id=p.id,
            title=p.title,
            objective=p.objective,
            project_type=p.project_type,
            needed_archetypes=p.needed_archetypes.split(",") if p.needed_archetypes else [],
            open_roles=p.open_roles,
            timeline=p.timeline,
            region=p.region,
            coalition_tags=p.coalition_tags.split(",") if p.coalition_tags else [],
            poster_id=p.poster_id,
            created_at=p.created_at
        )
        for p in projects
    ]


# ---------------------------------------------------------
# ✅ POST a new project
# ---------------------------------------------------------
@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    try:
        project_data = project.dict()
        project_data["needed_archetypes"] = ",".join(project_data.get("needed_archetypes", []))
        project_data["coalition_tags"] = ",".join(project_data.get("coalition_tags", []))

        new_project = models.Project(**project_data)
        db.add(new_project)
        db.commit()
        db.refresh(new_project)
        return new_project
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating project: {str(e)}")


# ---------------------------------------------------------
# ✅ GET single project by ID
# ---------------------------------------------------------
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse(
        id=project.id,
        title=project.title,
        objective=project.objective,
        project_type=project.project_type,
        needed_archetypes=project.needed_archetypes.split(",") if project.needed_archetypes else [],
        open_roles=project.open_roles,
        timeline=project.timeline,
        region=project.region,
        coalition_tags=project.coalition_tags.split(",") if project.coalition_tags else [],
        poster_id=project.poster_id,
        created_at=project.created_at
    )


# ---------------------------------------------------------
# ✅ DELETE a project
# ---------------------------------------------------------
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return {"message": f"✅ Project '{project.title}' deleted successfully"}

