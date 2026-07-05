from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    password: Mapped[str] = mapped_column(String(120))
    group_name: Mapped[str] = mapped_column(String(80), ForeignKey("groups.name"))
    role: Mapped[str] = mapped_column(String(80))
    mfa_required: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(40), default="有効")
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    group: Mapped[Group] = relationship()


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    app_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    sso_method: Mapped[str] = mapped_column(String(80))
    mfa_policy: Mapped[str] = mapped_column(String(80))
    target_groups: Mapped[str] = mapped_column(String(200))
    status: Mapped[str] = mapped_column(String(40), default="有効")
    last_auth_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160))
    condition: Mapped[str] = mapped_column(String(240))
    action: Mapped[str] = mapped_column(String(240))
    priority: Mapped[int] = mapped_column(Integer)


class AuthLog(Base):
    __tablename__ = "auth_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    application: Mapped[str] = mapped_column(String(160), index=True)
    auth_method: Mapped[str] = mapped_column(String(80))
    mfa_method: Mapped[str] = mapped_column(String(80))
    result: Mapped[str] = mapped_column(String(40), index=True)
    source_ip: Mapped[str] = mapped_column(String(80))
    risk: Mapped[str] = mapped_column(String(80))
    note: Mapped[str] = mapped_column(Text)


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True)
    state: Mapped[str] = mapped_column(String(40), default="mfa_pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
