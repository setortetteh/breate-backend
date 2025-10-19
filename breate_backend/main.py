from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from breate_backend import models
from breate_backend.database import engine, get_db, SessionLocal

# ✅ Import all routers
from breate_backend.routers import (
    user,
    archetype,
    tier,
    profile,
    auth,
    discover,
    projects,
    coalitions,
    collabcircle,  # ✅ NEW: Collab Circle routes
)

app = FastAPI(
    title="Breate API",
    version="1.0.0",
    description="Backend API for the Breate Web App",
)

# ---------------------------------------
# ✅ CORS Setup (fixed ports and origins)
# ---------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # ✅ Default Next.js dev port
        "http://127.0.0.1:3000",   # ✅ Alternate local IP
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3009",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------
# ✅ Database Initialization
# ---------------------------------------
print("🛠️ Ensuring all tables exist (no data will be dropped)...")
models.Base.metadata.create_all(bind=engine)
print("✅ Database schema checked and up to date.")

# ---------------------------------------
# ✅ Include Routers
# ---------------------------------------
app.include_router(user.router, prefix="/api/v1")
app.include_router(archetype.router, prefix="/api/v1")
app.include_router(tier.router, prefix="/api/v1")
app.include_router(profile.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(discover.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(coalitions.router, prefix="/api/v1")
app.include_router(collabcircle.router, prefix="/api/v1")  # ✅ NEW: Collab Circle router

# ---------------------------------------
# ✅ Root Route
# ---------------------------------------
@app.get("/", tags=["Root"])
def root():
    return {"message": "Welcome to the Breate API!"}

# ---------------------------------------
# ✅ Health Checks
# ---------------------------------------
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

@app.get("/health/db", tags=["Health"])
def check_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version();"))
        version = result.scalar()
        return {"status": "✅ Connected", "postgres_version": version}
    except Exception as e:
        return {"status": "❌ Connection failed", "error": str(e)}

# ---------------------------------------
# ✅ Seed Defaults (safe, non-destructive)
# ---------------------------------------
@app.on_event("startup")
def seed_default_data():
    db = SessionLocal()
    try:
        default_archetypes = [
            {"name": "Creator", "description": "Visionary builders who bring ideas to life."},
            {"name": "Creative", "description": "Expressive individuals skilled in storytelling and design."},
            {"name": "Innovator", "description": "Thinkers who challenge norms and create new approaches."},
            {"name": "Systems Thinker", "description": "Analytical minds who design scalable systems."},
        ]
        for archetype in default_archetypes:
            if not db.query(models.Archetype).filter_by(name=archetype["name"]).first():
                db.add(models.Archetype(**archetype))

        default_tiers = [
            {"name": "Base", "level": 1, "description": "Entry-level creators starting out."},
            {"name": "Standard", "level": 2, "description": "Intermediate users gaining experience."},
            {"name": "Professional", "level": 3, "description": "Experts with consistent contributions."},
        ]
        for tier in default_tiers:
            if not db.query(models.Tier).filter_by(name=tier["name"]).first():
                db.add(models.Tier(**tier))

        default_coalitions = [
            {
                "name": "Climate Action Network",
                "description": "A coalition focused on sustainable innovation and climate projects.",
                "focus": "Climate Change",
                "location": "Global",
            },
            {
                "name": "Tech for Good",
                "description": "Coalition uniting creators using technology to drive social impact.",
                "focus": "Innovation",
                "location": "Africa",
            },
        ]
        for coalition in default_coalitions:
            if not db.query(models.Coalition).filter_by(name=coalition["name"]).first():
                db.add(models.Coalition(**coalition))

        db.commit()
        print("✅ Default archetypes, tiers, and coalitions seeded successfully.")
    except Exception as e:
        print("❌ Error seeding data:", str(e))
    finally:
        db.close()

