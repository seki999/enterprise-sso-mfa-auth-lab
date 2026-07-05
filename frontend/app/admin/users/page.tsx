"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../../nav";
import { apiGet } from "../../../lib/api";

type User = { user_id: string; name: string; group: string; role: string; mfa: string; status: string; last_login_at: string | null };

export default function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [message, setMessage] = useState("");
  useEffect(() => { apiGet<User[]>("/users").then(setUsers); }, []);

  return (
    <AppShell>
      <div className="page-header">
        <div><h1 className="page-title">ユーザー管理</h1><p className="page-lead">架空ユーザーの状態、ロール、MFA適用状況を確認します。</p></div>
      </div>
      {message && <div className="message">{message}</div>}
      <section className="panel table-wrap">
        <table><thead><tr><th>ユーザーID</th><th>名前</th><th>グループ</th><th>ロール</th><th>MFA</th><th>状態</th><th>最終ログイン</th><th>操作</th></tr></thead>
          <tbody>{users.map((user) => <tr key={user.user_id}><td>{user.user_id}</td><td>{user.name}</td><td>{user.group}</td><td>{user.role}</td><td>{user.mfa}</td><td><span className={`status ${user.status === "有効" ? "ok" : "ng"}`}>{user.status}</span></td><td>{user.last_login_at ?? "-"}</td><td><div className="actions"><button onClick={() => setMessage(`${user.name} を有効化しました（デモ）`)}>有効化</button><button className="secondary" onClick={() => setMessage(`${user.name} を無効化しました（デモ）`)}>無効化</button><button className="secondary" onClick={() => setMessage(`${user.name} のMFA再登録を開始しました（デモ）`)}>MFA再登録</button><button className="secondary" onClick={() => setMessage(`${user.name} のポリシーを確認しました（デモ）`)}>ポリシー確認</button></div></td></tr>)}</tbody></table>
      </section>
    </AppShell>
  );
}
