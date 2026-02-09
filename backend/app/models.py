from enum import auto
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, JSON, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime, timezone
from .database import Base

class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nct_id = Column(String(20), unique=True, index=True, nullable=False)
    brief_title = Column(Text)
    official_title = Column(Text)
    overall_status = Column(String(50))
    phase = Column(String(50))
    study_type = Column(String(50))

    # Eligibility criteria
    eligibility_criteria = Column(LONGTEXT)
    gender = Column(String(20))
    minimum_age = Column(String(20))
    maximum_age = Column(String(20))

    # Dates
    start_date = Column(Date)
    primary_completion_date = Column(Date)
    completion_date = Column(Date)
    first_posted = Column(Date)
    last_update_posted = Column(Date)

    # JSON columns
    detailed_description = Column(JSON)
    arms_goups = Column(JSON)
    outcomes = Column(JSON)
    contacts = Column(JSON)


    from datetime import datetime
    created_at = Column(Date, default=datetime.now(datetime.timezone.utc))
    updated_at = Column(Date, default=datetime.now(datetime.timezone.utc), onupdate=datetime.now(datetime.timezone.utc))

    # Relationships
    conditions = relationship("Condition", secondary="trial_conditions", back_populates="trials")
    interventions = relationship("Intervention", secondary="trial_intervention", back_populates="trials")
    locations = relationship("Location", back_populates="trial")

class Condition(Base):
    __tablename__ = "conditions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), index=True)
    normalized_name = Column(String(500), index=True)

    trials = relationship("Trial", secondary="trial_conditions", back_populates="conditions")

class Intervention(Base):
    __tablename__ = "interventions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    intervention_type = Column(String(100))
    name = Column(String(500))
    description = Column(Text)

    trials = relationship("Trial", secondary="trial_interventions", back_populates="interventions")

class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trial_id = Column(Integer, ForeignKey("trials.id", ondelete="CASCADE"))
    facility = Column(String(500))
    city = Column(String(200))
    state = Column(String(200))
    country = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)

    trial = relationship("Trial", back_populates="locations")

# Association tables
from sqlalchemy import Table
trial_conditions = Table(
    "trial_conditions",
    Base.metadata,
    Column("trial_id", Integer, ForeignKey("trials.id", ondelete="CASCADE")),
    Column("conditions_id", Integer, ForeignKey("conditions.id", ondelete="CASCADE")),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4"
)

trial_interventions = Table(
    "trial_interventions",
    Base.metadata,
    Column("trial_id", Integer, ForeignKey("trials.id", ondelete="CASCADE")),
    Column("intervention_id", Integer, ForeignKey("interventions.id", ondelete="CASCADE")),
    mysql_engine="InnoDB",
    mysql_charset="utf8mb4"
)