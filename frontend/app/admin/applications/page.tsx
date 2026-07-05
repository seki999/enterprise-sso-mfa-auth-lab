"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../../nav";
import { apiGet } from "../../../lib/api";

type AppItem = { app_id: string; name: string; sso_method: string; mfa_policy: string; target_groups: string; status: string; last_auth_at: string | null };

export default function ApplicationsPage() {
  const [apps, setApps] = useState<AppItem[]>([]);
  useEffect(() => { apiGet<AppItem[]>("/applications").then(setApps); }, []);
  return (
    <AppShell>
      <div className="page-header"><div><h1 className="page-title">アプリケーション管理</h1><p className="page-lead">SSO対象アプリケーションとMFA適用方針を確認します。</p></div></div>
      <section className="panel table-wrap">
        <table><thead><tr><th>アプリID</th><th>アプリケーション名</th><th>SSO方式</th><th>MFA</th><th>対象グループ</th><th>状態</th><th>最終認証日時</th></tr></thead>
          <tbody>{apps.map((app) => <tr key={app.app_id}><td>{app.app_id}</td><td>{app.name}</td><td>{app.sso_method}</td><td>{app.mfa_policy}</td><td>{app.target_groups}</td><td><span className="status ok">{app.status}</span></td><td>{app.last_auth_at ?? "-"}</td></tr>)}</tbody></table>
      </section>
    </AppShell>
  );
}
