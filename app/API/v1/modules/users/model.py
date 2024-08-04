from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base, TimestampMixin, SoftDeleteMixin

class AcceptedTerms(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "accepted_terms"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(500), nullable=False)

class Role(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False, unique=True)

    # One-to-one relationship with User
    user = relationship("User", back_populates="role", uselist=False)

class User(Base, SoftDeleteMixin, TimestampMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(60), nullable=False)
    email = Column(String(60), nullable=False, unique=True)
    phone = Column(String(60), nullable=False)
    password = Column(String(100), nullable=False)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # One-to-one relationship with Role
    role = relationship("Role", back_populates="user")

    
