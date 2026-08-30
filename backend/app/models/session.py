# Security ans Session

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.core.database.base import BaseModel


class PortalSession(BaseModel):
    __tablename__ = "portal_session"

    # Session information
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    portal_id = Column(Integer, ForeignKey("educational_portal.id"), nullable=False)
    session_token = Column(String(255), unique=True, nullable=False)

    # Timing
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)

    # Status
    status = Column(
        String(50), default="active"
    )  # active, completed, expired, terminated
    termination_reason = Column(String(255), nullable=True)

    # Security
    ip_address = Column(String(45), nullable=False)
    user_agent = Column(Text, nullable=True)
    security_level = Column(
        String(50), default="standard"
    )  # standard, enhanced, strict

    # Activity tracking
    activity_log = Column(JSON, nullable=True)  # Stores session activities

    # Relationship
    user = relationship("User", back_populates=True)
    portal = relationship("EducationalPortal", back_populates="sessions")

    def __repr__(self):
        return f"<PortalSession(id={self.id}, user.id={self.user_id}, status={self.status})>"


class EducationalPortal(BaseModel):
    __tablename__ = "educational_portals"

    name = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)  # 'University', 'tvt', 'schools'
    requires_credentials = Column(JSON, nullable=True)
    security_config = Column(Integer, ForeignKey("institution.id"), nullable=True)

    # Relationships
    institution = relationship("Institution", back_populates="portals")
    sessions = relationship("PortalSession", back_populates="portal")

    def __repr__(self):
        return f"<EducationalPortal(id={self.id}, name={self.name})>"
