from datetime import date, datetime

from sqlalchemy import (Boolean, Column, Date, DateTime, Float, ForeignKey,
                        Integer, String, Text, create_engine)
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker

from backend.config import SQLITE_PATH


class Base(DeclarativeBase):
    pass


class ChildProfile(Base):
    __tablename__ = "child_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    family_id = Column(String(64), nullable=False, index=True)
    name_encrypted = Column(Text, nullable=False)
    dob = Column(Date, nullable=False)
    sex = Column(String(10), nullable=False)
    health_notes_encrypted = Column(Text, default="")
    preferred_language = Column(String(8), default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    milestones = relationship("MilestoneLog", back_populates="child", cascade="all, delete-orphan")
    growth_logs = relationship("GrowthLog", back_populates="child", cascade="all, delete-orphan")


class MilestoneLog(Base):
    __tablename__ = "milestone_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"), nullable=False, index=True)
    domain = Column(String(32), nullable=False)
    milestone_label = Column(String(128), nullable=False)
    achieved_date = Column(Date, nullable=False)
    notes_encrypted = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("ChildProfile", back_populates="milestones")


class GrowthLog(Base):
    __tablename__ = "growth_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"), nullable=False, index=True)
    measured_date = Column(Date, nullable=False)
    weight_kg = Column(Float, nullable=True)
    height_cm = Column(Float, nullable=True)
    head_circumference_cm = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    child = relationship("ChildProfile", back_populates="growth_logs")


class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, autoincrement=True)
    child_id = Column(Integer, ForeignKey("child_profiles.id"), nullable=False, index=True)
    session_id = Column(String(64), nullable=False, index=True)
    role = Column(String(16), nullable=False)
    content_encrypted = Column(Text, nullable=False)
    emotion = Column(String(32), nullable=True)
    evidence_level = Column(String(32), nullable=True)
    safety_triggered = Column(Boolean, default=False)
    llm_provider_used = Column(String(32), nullable=True)
    token_count = Column(Integer, default=0)
    cost_estimate = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class CrawlLog(Base):
    __tablename__ = "crawl_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(64), nullable=False)
    papers_found = Column(Integer, default=0)
    papers_added = Column(Integer, default=0)
    topics = Column(Text, default="")
    notable_findings = Column(Text, default="")
    status = Column(String(16), default="success")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_engine(f"sqlite:///{SQLITE_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
