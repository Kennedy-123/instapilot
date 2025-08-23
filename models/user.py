from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String(80), unique=True, nullable=False)
    facebook_name = Column(String(80), nullable=False, unique=True)
    facebook_access_token = Column(String(512))
    facebook_id = Column(String(80), nullable=False, unique=True)
    facebook_token_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = relationship(
        "Post", 
        back_populates="author", 
        cascade="all, delete-orphan"
    )
