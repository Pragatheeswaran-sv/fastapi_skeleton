import uuid
from datetime import datetime, timezone
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from src.database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID, primary_key = True, default = uuid.uuid4)
    name = Column(Text)
    email_address = Column(String(255), nullable = False)
    password_hash = Column(String(255), nullable = False)
    phone_number = Column(String(20), nullable = True)
    created_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), nullable = False)
    updated_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc), nullable = False)
    created_by = Column(String, nullable = True)
    updated_by = Column(String, nullable = True)
    is_active = Column(Boolean, default = True)


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    token_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    jti = Column(String(255), nullable=False, unique=True, index=True)
    token = Column(Text,nullable=False)
    expires_at = Column(DateTime(timezone=True),nullable=False)
    is_revoked = Column(Boolean,default=False,nullable=False)
    revoked_at = Column(DateTime(timezone=True),nullable=True)
    created_at = Column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)
    updated_at = Column(DateTime(timezone = True), default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc), nullable = False)
    created_by = Column(String, nullable = True)
    updated_by = Column(String, nullable = True)

    # users = relationship("users")
