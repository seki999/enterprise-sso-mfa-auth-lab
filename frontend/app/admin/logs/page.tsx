"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../../nav";
import { apiGet } from "../../../lib/api";

type Log = { id: number; occurred_at: string; user_id: string; application: string; auth_method: string; mfa_method: string; result: string; source_ip: string; risk: string; note: string };

export default function LogsPage() {
  const [logs, setLogs] = useState<Log[]>([]);
  const [userId, setUserId] = useState("");
  const [result, setResult] = useState("");

  async function load() {
    const params = new URLSearchParams();
    if (userId) params.set("user_id", userId);
    if (result) params.set("result", result);
    const query = params.toString();
    setLogs(await apiGet<Log[]>(`/auth-logs${query ? `?${query}` : ""}`));
  }

  useEffect(() => { load(); }, []);

  return (
    <AppShell>
      <div className="page-header"><div><h1 className="page-title">認証ログ / 監査ログ</h1><p className="page-lead">成功、失敗、拒否、ロックをSQLiteに記録し、調査観点を確認します。</p></div></div>
      <section className="panel">
        <div className="actions">
          <input placeholder="ユーザーID" value={userId} onChange={(e) => setUserId(e.target.value)} />
          <select value={result} onChange={(e) => setResult(e.target.value)}><option value="">結果すべて</option><option>成功</option><option>失敗</option><option>拒否</option><option>ロック</option></select>
          <button onClick={load}>フィルター</button>
        </div>
      </section>
      <section className="panel table-wrap">
        <table><thead><tr><th>日時</th><th>ユーザー</th><th>アプリ</th><th>認証方式</th><th>MFA方式</th><th>結果</th><th>IP</th><th>リスク</th><th>備考</th></tr></thead>
          <tbody>{logs.map((log) => <tr key={log.id}><td>{log.occurred_at}</td><td>{log.user_id}</td><td>{log.application}</td><td>{log.auth_method}</td><td>{log.mfa_method}</td><td><span className={`status ${log.result === "成功" ? "ok" : log.result === "失敗" ? "warn" : "ng"}`}>{log.result}</span></td><td>{log.source_ip}</td><td>{log.risk}</td><td>{log.note}</td></tr>)}</tbody></table>
      </section>
    </AppShell>
  );
}
