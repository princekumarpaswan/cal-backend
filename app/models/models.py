from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer, Table
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import uuid


# Association table for family group members
family_members = Table(
    'family_members',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('family_group_id', UUID(as_uuid=True), ForeignKey('family_groups.id', ondelete='CASCADE')),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('role', String(20), default='member'),  # owner, admin, member
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
)


# Association table for event attendees
event_attendees = Table(
    'event_attendees',
    Base.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('event_id', UUID(as_uuid=True), ForeignKey('events.id', ondelete='CASCADE')),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE')),
    Column('status', String(20), default='pending'),  # pending, accepted, declined
)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email_verified = Column(Boolean, default=False)
    phone = Column(String(50), nullable=True)
    avatar_url = Column(Text, nullable=True)
    timezone = Column(String(100), default='UTC')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owned_groups = relationship("FamilyGroup", back_populates="owner", foreign_keys="FamilyGroup.owner_id")
    family_groups = relationship("FamilyGroup", secondary=family_members, back_populates="members")
    created_events = relationship("Event", back_populates="creator", foreign_keys="Event.created_by")
    attending_events = relationship("Event", secondary=event_attendees, back_populates="attendees")
    created_tasks = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")
    assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")


class FamilyGroup(Base):
    __tablename__ = "family_groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="owned_groups", foreign_keys=[owner_id])
    members = relationship("User", secondary=family_members, back_populates="family_groups")
    events = relationship("Event", back_populates="family_group", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="family_group", cascade="all, delete-orphan")
    invitations = relationship("FamilyInvitation", back_populates="family_group", cascade="all, delete-orphan")


class FamilyInvitation(Base):
    __tablename__ = "family_invitations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    family_group_id = Column(UUID(as_uuid=True), ForeignKey('family_groups.id', ondelete='CASCADE'), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    role = Column(String(20), default='member')
    status = Column(String(20), default='pending')  # pending, accepted, declined, expired
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    family_group = relationship("FamilyGroup", back_populates="invitations")


class Event(Base):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    location = Column(Text, nullable=True)
    color = Column(String(7), default='#3B82F6')
    recurrence = Column(JSONB, nullable=True)  # JSON object for recurrence rules
    reminders = Column(JSONB, nullable=True)  # JSON array for reminders
    family_group_id = Column(UUID(as_uuid=True), ForeignKey('family_groups.id', ondelete='CASCADE'), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    creator = relationship("User", back_populates="created_events", foreign_keys=[created_by])
    attendees = relationship("User", secondary=event_attendees, back_populates="attending_events")
    family_group = relationship("FamilyGroup", back_populates="events")
    linked_tasks = relationship("Task", back_populates="linked_event")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    priority = Column(String(20), default='medium')  # low, medium, high
    status = Column(String(20), default='pending')  # pending, in_progress, completed, cancelled
    assigned_to = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    linked_event_id = Column(UUID(as_uuid=True), ForeignKey('events.id', ondelete='SET NULL'), nullable=True)
    family_group_id = Column(UUID(as_uuid=True), ForeignKey('family_groups.id', ondelete='CASCADE'), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[created_by])
    linked_event = relationship("Event", back_populates="linked_tasks")
    family_group = relationship("FamilyGroup", back_populates="tasks")

