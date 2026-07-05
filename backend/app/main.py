from __future__ import annotations

import os
import secrets
from datetime import datetime

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session as DbSession

from .database import Base, engine, get_db
from .models import Application, AuthLog, Policy, Session, User
from .schemas import LoginRequest, LoginResponse, MfaRequest, MessageResponse, VpnLoginRequest
from .seed import seed_database


Base.metadata.create_all(bind=engine)
seed_database()

app = FastAPI(title="企業向けSSO/MFA認証基盤ラボAPI")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def log_event(db: DbSession, user_id: str, application: str, result: str, note: str, auth_method: str = "Mock SSO", mfa_method: str = "未実施") -> None:
    db.add(
        AuthLog(
            user_id=user_id,
            application=application,
            auth_method=auth_method,
            mfa_method=mfa_method,
            result=result,
            source_ip="10.0.0.25",
            risk="低" if result == "成功" else "高",
            note=note,
        )
    )
    db.commit()


def serialize_user(user: User) -> dict:
    return {
        "user_id": user.user_id,
        "name": user.name,
        "group": user.group_name,
        "role": user.role,
        "mfa": "必須" if user.mfa_required else "任意",
        "status": user.status,
        "last_login_at": user.last_login_at,
    }


def list_auth_logs(db: DbSession, user_id: str | None = None, application: str | None = None, result: str | None = None) -> list[dict]:
    query = db.query(AuthLog)
    if user_id:
        query = query.filter(AuthLog.user_id.contains(user_id))
    if application:
        query = query.filter(AuthLog.application.contains(application))
    if result:
        query = query.filter(AuthLog.result == result)
    return [
        {
            "id": log.id,
            "occurred_at": log.occurred_at,
            "user_id": log.user_id,
            "application": log.application,
            "auth_method": log.auth_method,
            "mfa_method": log.mfa_method,
            "result": log.result,
            "source_ip": log.source_ip,
            "risk": log.risk,
            "note": log.note,
        }
        for log in query.order_by(AuthLog.occurred_at.desc()).limit(100).all()
    ]


def current_user(authorization: str | None = Header(default=None), db: DbSession = Depends(get_db)) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証トークンがありません")
    token = authorization.removeprefix("Bearer ").strip()
    session = db.query(Session).filter(Session.token == token, Session.state == "authenticated").first()
    if not session:
        raise HTTPException(status_code=401, detail="有効なセッションがありません")
    user = db.query(User).filter(User.user_id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="ユーザーが見つかりません")
    return user


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "message": "APIは正常に稼働しています", "auth_mode": os.getenv("AUTH_MODE", "mock")}


@app.post("/auth/login", response_model=LoginResponse)
def login(request: LoginRequest, db: DbSession = Depends(get_db)) -> LoginResponse:
    user = db.query(User).filter(User.user_id == request.user_id).first()
    if not user or user.password != request.password:
        log_event(db, request.user_id, "業務ダッシュボード", "失敗", "ユーザーIDまたはパスワードが一致しません")
        return LoginResponse(success=False, message="ユーザーIDまたはパスワードが正しくありません")
    if user.status != "有効":
        log_event(db, user.user_id, "業務ダッシュボード", "ロック", "アカウントが有効ではありません")
        return LoginResponse(success=False, message="アカウントがロックまたは無効です")

    token = secrets.token_urlsafe(32)
    db.add(Session(token=token, user_id=user.user_id, state="mfa_pending"))
    db.commit()
    return LoginResponse(success=True, message="Mock SSO認証に成功しました。MFAを実施してください。", token=token, next_step="mfa")


@app.post("/auth/mfa/verify", response_model=LoginResponse)
def verify_mfa(request: MfaRequest, db: DbSession = Depends(get_db)) -> LoginResponse:
    session = db.query(Session).filter(Session.token == request.token, Session.state == "mfa_pending").first()
    if not session:
        return LoginResponse(success=False, message="MFA待ちのセッションが見つかりません")
    if not request.approve and request.code != "123456":
        log_event(db, session.user_id, "業務ダッシュボード", "拒否", "Mock MFAコードが不一致でした", mfa_method="6桁コード")
        return LoginResponse(success=False, message="MFA認証に失敗しました")

    session.state = "authenticated"
    user = db.query(User).filter(User.user_id == session.user_id).first()
    if user:
        user.last_login_at = datetime.utcnow()
    log_event(db, session.user_id, "業務ダッシュボード", "成功", "Mock SSO + Mock MFAに成功しました", mfa_method="承認ボタン" if request.approve else "6桁コード")
    db.commit()
    return LoginResponse(success=True, message="MFA認証に成功しました", token=request.token, next_step="dashboard")


@app.post("/auth/logout", response_model=MessageResponse)
def logout(authorization: str | None = Header(default=None), db: DbSession = Depends(get_db)) -> MessageResponse:
    if authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ").strip()
        session = db.query(Session).filter(Session.token == token).first()
        if session:
            db.delete(session)
            db.commit()
    return MessageResponse(success=True, message="ログアウトしました")


@app.get("/me")
def me(user: User = Depends(current_user)) -> dict:
    return serialize_user(user)


@app.get("/users")
def users(db: DbSession = Depends(get_db)) -> list[dict]:
    return [serialize_user(user) for user in db.query(User).order_by(User.user_id).all()]


@app.get("/users/{user_id}")
def user_detail(user_id: str, db: DbSession = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    return serialize_user(user)


@app.get("/applications")
def applications(db: DbSession = Depends(get_db)) -> list[dict]:
    return [
        {
            "app_id": app_item.app_id,
            "name": app_item.name,
            "sso_method": app_item.sso_method,
            "mfa_policy": app_item.mfa_policy,
            "target_groups": app_item.target_groups,
            "status": app_item.status,
            "last_auth_at": app_item.last_auth_at,
        }
        for app_item in db.query(Application).order_by(Application.app_id).all()
    ]


@app.get("/policies")
def policies(db: DbSession = Depends(get_db)) -> list[dict]:
    return [
        {"id": policy.id, "name": policy.name, "condition": policy.condition, "action": policy.action, "priority": policy.priority}
        for policy in db.query(Policy).order_by(Policy.priority).all()
    ]


@app.get("/auth-logs")
def auth_logs(
    user_id: str | None = Query(default=None),
    application: str | None = Query(default=None),
    result: str | None = Query(default=None),
    db: DbSession = Depends(get_db),
) -> list[dict]:
    return list_auth_logs(db, user_id=user_id, application=application, result=result)


@app.post("/vpn/login", response_model=MessageResponse)
def vpn_login(request: VpnLoginRequest, db: DbSession = Depends(get_db)) -> MessageResponse:
    user = db.query(User).filter(User.user_id == request.user_id).first()
    if not user or user.password != request.password or user.status != "有効":
        log_event(db, request.user_id, "VPNログインシミュレーター", "失敗", "LDAP/AD相当のユーザー確認に失敗しました", auth_method="RADIUS想定")
        return MessageResponse(success=False, message="VPNログインに失敗しました")
    if not request.approve_mfa:
        log_event(db, user.user_id, "VPNログインシミュレーター", "拒否", "MFA承認が行われませんでした", auth_method="RADIUS想定")
        return MessageResponse(success=False, message="MFA承認が必要です")
    user.last_login_at = datetime.utcnow()
    log_event(db, user.user_id, "VPNログインシミュレーター", "成功", "RADIUS + LDAP/AD + MFA想定のVPN認証に成功しました", auth_method="RADIUS想定", mfa_method="承認ボタン")
    return MessageResponse(success=True, message="VPNログインに成功しました")


@app.get("/dashboard/summary")
def dashboard_summary(user: User = Depends(current_user), db: DbSession = Depends(get_db)) -> dict:
    apps = db.query(Application).filter(Application.target_groups.contains(user.group_name)).all()
    recent_logs = list_auth_logs(db, user_id=user.user_id)[:5]
    return {
        "user": serialize_user(user),
        "auth_method": os.getenv("AUTH_MODE", "mock"),
        "mfa_method": "Mock MFA",
        "security_status": "MFA適用済み / セッション有効",
        "applications": [
            {"app_id": app_item.app_id, "name": app_item.name, "sso_method": app_item.sso_method, "mfa_policy": app_item.mfa_policy}
            for app_item in apps
        ],
        "recent_logs": recent_logs,
    }
