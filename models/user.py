from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    facebook_name = Column(String(80), nullable=False, unique=True)
    facebook_access_token = Column(String(512))
    instagram_id = Column(String(80), nullable=True, unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    posts = relationship(
        "Post", 
        back_populates="author", 
        cascade="all, delete-orphan"
    )
