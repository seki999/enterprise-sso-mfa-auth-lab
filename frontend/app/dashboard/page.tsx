"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../nav";
import { apiGet, getToken } from "../../lib/api";

type Summary = {
  user: { user_id: string; name: string; group: string; role: string; last_login_at: string | null };
  auth_method: string;
  mfa_method: string;
  security_status: string;
  applications: { app_id: string; name: string; sso_method: string; mfa_policy: string }[];
  recent_logs: { occurred_at: string; application: string; result: string; note: string }[];
};

export default function DashboardPage() {
  const [summary, setSummary] = useState<Summary | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    apiGet<Summary>("/dashboard/summary", getToken()).then(setSummary).catch(() => setError("ログイン後に表示してください"));
  }, []);

  return (
    <AppShell>
      <div className="page-header">
        <div>
          <h1 className="page-title">業務ダッシュボード</h1>
          <p className="page-lead">認証済みユーザーの利用可能アプリと直近ログを表示します。</p>
        </div>
      </div>
      {error && <div className="message">{error}</div>}
      {summary && (
        <div className="grid">
          <div className="grid cols-3">
            <section className="panel"><div className="metric">ログインユーザー</div><div className="metric-value">{summary.user.name}</div><p>{summary.user.group} / {summary.user.role}</p></section>
            <section className="panel"><div className="metric">認証方式</div><div className="metric-value">{summary.auth_method}</div><p>MFA方式: {summary.mfa_method}</p></section>
            <section className="panel"><div className="metric">セキュリティ状態</div><div className="metric-value">{summary.security_status}</div><p>最終ログイン: {summary.user.last_login_at ?? "未記録"}</p></section>
          </div>
          <section className="panel">
            <h2>アクセス可能なアプリケーション</h2>
            <div className="table-wrap"><table><thead><tr><th>アプリ</th><th>方式</th><th>MFA</th></tr></thead><tbody>{summary.applications.map((app) => <tr key={app.app_id}><td>{app.name}</td><td>{app.sso_method}</td><td>{app.mfa_policy}</td></tr>)}</tbody></table></div>
          </section>
          <section className="panel">
            <h2>直近5件の認証ログ</h2>
            <div className="table-wrap"><table><thead><tr><th>日時</th><th>アプリ</th><th>結果</th><th>備考</th></tr></thead><tbody>{summary.recent_logs.map((log, i) => <tr key={i}><td>{log.occurred_at}</td><td>{log.application}</td><td><span className={`status ${log.result === "成功" ? "ok" : "ng"}`}>{log.result}</span></td><td>{log.note}</td></tr>)}</tbody></table></div>
          </section>
        </div>
      )}
    </AppShell>
  );
}
