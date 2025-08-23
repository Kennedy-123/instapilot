from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime, timezone

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    media_url = Column(String(200), nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign Key
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship (requires User model to also be defined)
    author = relationship("User", back_populates="posts")
