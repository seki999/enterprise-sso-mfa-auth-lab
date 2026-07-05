from __future__ import annotations

from datetime import datetime, timedelta

from .database import Base, SessionLocal, engine
from .models import Application, AuthLog, Group, Policy, User


def seed_database(force: bool = False) -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if force:
            for model in (AuthLog, Policy, Application, User, Group):
                db.query(model).delete()
            db.commit()
        if db.query(User).first():
            return

        groups = [
            Group(name="administrators", display_name="管理者"),
            Group(name="employees", display_name="一般社員"),
            Group(name="contractors", display_name="契約社員"),
        ]
        db.add_all(groups)

        users = [
            User(user_id="admin01", name="管理者 太郎", password="Password123!", group_name="administrators", role="管理者", mfa_required=True, status="有効"),
            User(user_id="employee01", name="社員 花子", password="Password123!", group_name="employees", role="一般社員", mfa_required=True, status="有効"),
            User(user_id="employee02", name="社員 一郎", password="Password123!", group_name="employees", role="一般社員", mfa_required=True, status="有効"),
            User(user_id="contractor01", name="協力会社 健", password="Password123!", group_name="contractors", role="契約社員", mfa_required=True, status="有効"),
            User(user_id="locked01", name="ロック 太郎", password="Password123!", group_name="employees", role="一般社員", mfa_required=True, status="ロック中"),
        ]
        db.add_all(users)

        now = datetime.utcnow().replace(microsecond=0)
        apps = [
            Application(app_id="app-portal", name="社内ポータル", sso_method="OIDC", mfa_policy="必須", target_groups="employees, administrators", status="有効", last_auth_at=now - timedelta(hours=2)),
            Application(app_id="app-dashboard", name="業務ダッシュボード", sso_method="OIDC", mfa_policy="必須", target_groups="employees, administrators", status="有効", last_auth_at=now - timedelta(hours=1)),
            Application(app_id="app-admin", name="管理者コンソール", sso_method="SAML想定", mfa_policy="強制", target_groups="administrators", status="有効", last_auth_at=now - timedelta(days=1)),
            Application(app_id="app-contractor", name="契約社員向け申請システム", sso_method="OIDC", mfa_policy="必須", target_groups="contractors", status="有効", last_auth_at=now - timedelta(days=2)),
            Application(app_id="app-vpn", name="VPNログインシミュレーター", sso_method="RADIUS想定", mfa_policy="必須", target_groups="employees, administrators", status="有効", last_auth_at=now - timedelta(minutes=40)),
        ]
        db.add_all(apps)

        policies = [
            Policy(name="管理者MFA必須", condition="role == 管理者", action="常にMFAを要求", priority=10),
            Policy(name="社外アクセスMFA", condition="source != 社内ネットワーク", action="一般社員にMFAを要求", priority=20),
            Policy(name="契約社員アプリ制限", condition="group == contractors", action="許可アプリのみアクセス可", priority=30),
            Policy(name="失敗回数ロック", condition="failed_count > 5", action="アカウントをロック", priority=40),
            Policy(name="管理者コンソール強力MFA", condition="application == 管理者コンソール", action="Verified Push相当を要求", priority=50),
            Policy(name="VPN RADIUS MFA", condition="application == VPN", action="RADIUS + MFAを要求", priority=60),
        ]
        db.add_all(policies)

        results = ["成功", "失敗", "拒否", "ロック"]
        users_cycle = ["admin01", "employee01", "employee02", "contractor01", "locked01"]
        apps_cycle = ["業務ダッシュボード", "社内ポータル", "管理者コンソール", "契約社員向け申請システム", "VPNログインシミュレーター"]
        logs = []
        for i in range(24):
            result = results[i % len(results)]
            logs.append(
                AuthLog(
                    occurred_at=now - timedelta(minutes=17 * i),
                    user_id=users_cycle[i % len(users_cycle)],
                    application=apps_cycle[i % len(apps_cycle)],
                    auth_method="Mock SSO" if i % 5 else "RADIUS想定",
                    mfa_method="6桁コード" if i % 3 else "承認ボタン",
                    result=result,
                    source_ip=f"10.10.{i % 5}.{20 + i}",
                    risk="低" if result == "成功" else ("中" if result == "失敗" else "高"),
                    note="seedデータ: 検証用の架空ログ",
                )
            )
        db.add_all(logs)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database(force=True)
    print("seedデータを投入しました")
