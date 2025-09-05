from sqlalchemy import Column, BigInteger, Text, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import Base
from datetime import datetime, timezone

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    media_url = Column(Text, nullable=True)  # better to explicitly set type
    scheduled_time = Column(DateTime, nullable=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign Key
    author_id = Column(BigInteger, ForeignKey('users.telegram_id'), nullable=False)

    # Relationship
    author = relationship("User", back_populates="posts")
