from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    password: str


class MfaRequest(BaseModel):
    token: str
    code: str | None = None
    approve: bool = False


class VpnLoginRequest(BaseModel):
    user_id: str
    password: str
    approve_mfa: bool = False


class MessageResponse(BaseModel):
    success: bool
    message: str


class LoginResponse(MessageResponse):
    token: str | None = None
    next_step: str | None = None


class UserResponse(BaseModel):
    user_id: str
    name: str
    group: str
    role: str
    mfa: str
    status: str
    last_login_at: datetime | None


class ApplicationResponse(BaseModel):
    app_id: str
    name: str
    sso_method: str
    mfa_policy: str
    target_groups: str
    status: str
    last_auth_at: datetime | None
