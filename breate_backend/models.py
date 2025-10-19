from sqlalchemy import Column, Integer, String, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from breate_backend.database import Base

# ------------------------------------------------------
# ✅ Association table for coalition members (many-to-many)
# ------------------------------------------------------
coalition_members = Table(
    "coalition_members",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
    Column("coalition_id", Integer, ForeignKey("coalitions.id", ondelete="CASCADE")),
)

# ------------------------------------------------------
# ✅ Archetype Model
# ------------------------------------------------------
class Archetype(Base):
    __tablename__ = "archetypes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="archetype")


# ------------------------------------------------------
# ✅ Tier Model
# ------------------------------------------------------
class Tier(Base):
    __tablename__ = "tiers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    level = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", back_populates="tier")


# ------------------------------------------------------
# ✅ User Model
# ------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    username = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    preferred_themes = Column(Text, nullable=True)
    portfolio_links = Column(Text, nullable=True)
    next_build = Column(Text, nullable=True)
    affiliations = Column(Text, nullable=True)

    archetype_id = Column(Integer, ForeignKey("archetypes.id"))
    tier_id = Column(Integer, ForeignKey("tiers.id"))

    archetype = relationship("Archetype", back_populates="users")
    tier = relationship("Tier", back_populates="users")

    # Coalitions this user is part of
    coalitions = relationship("Coalition", secondary=coalition_members, back_populates="members")

    # Projects this user posted
    projects = relationship("Project", back_populates="poster")


# ------------------------------------------------------
# ✅ Coalition Model (no creator_id)
# ------------------------------------------------------
class Coalition(Base):
    __tablename__ = "coalitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    focus = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Members (many-to-many)
    members = relationship("User", secondary=coalition_members, back_populates="coalitions")


# ------------------------------------------------------
# ✅ Project Model
# ------------------------------------------------------
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    objective = Column(Text, nullable=False)
    project_type = Column(String, nullable=False)
    needed_archetypes = Column(Text, nullable=False)  # comma-separated list
    open_roles = Column(Text, nullable=True)
    timeline = Column(String, nullable=True)
    region = Column(String, nullable=True)
    coalition_tags = Column(Text, nullable=True)  # comma-separated list
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    poster_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    poster = relationship("User", back_populates="projects")


# ------------------------------------------------------
# ✅ Collab Circle (Verified Collaboration Links)
# ------------------------------------------------------
class CollabLink(Base):
    __tablename__ = "collab_links"

    id = Column(Integer, primary_key=True, index=True)
    user_a_username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    user_b_username = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable=False)
    project_name = Column(String, nullable=True)
    status = Column(String, default="pending")  # "pending" or "verified"
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())












