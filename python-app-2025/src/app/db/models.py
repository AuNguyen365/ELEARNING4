from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.session import Base


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True, nullable=False)
	username = Column(String, unique=True, index=True, nullable=False)
	hashed_password = Column(String, nullable=False)
	is_active = Column(Boolean, default=True)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	blogs = relationship("Blog", back_populates="author")


class Blog(Base):
	__tablename__ = "blogs"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True, nullable=False)
	content = Column(Text, nullable=False)
	tags = Column(String, nullable=True)  # comma-separated tags
	image = Column(String, nullable=True)
	created_at = Column(DateTime, default=datetime.utcnow)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
	author = relationship("User", back_populates="blogs")

