"use client";

import { useState } from "react";
import { AppShell } from "../nav";
import { apiPost } from "../../lib/api";

type Response = { success: boolean; message: string };

export default function VpnLoginPage() {
  const [userId, setUserId] = useState("employee01");
  const [password, setPassword] = useState("Password123!");
  const [approveMfa, setApproveMfa] = useState(true);
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const result = await apiPost<Response>("/vpn/login", { user_id: userId, password, approve_mfa: approveMfa });
    setMessage(result.message);
  }

  return (
    <AppShell>
      <div className="page-header"><div><h1 className="page-title">VPNログインシミュレーター</h1><p className="page-lead">Duo Authentication Proxy + RADIUS + LDAP / AD連携を想定した検証画面です。</p></div></div>
      <section className="panel">
        <form className="form" onSubmit={submit}>
          <label>ユーザーID<input value={userId} onChange={(e) => setUserId(e.target.value)} /></label>
          <label>パスワード<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
          <label><span><input type="checkbox" checked={approveMfa} onChange={(e) => setApproveMfa(e.target.checked)} /> MFA承認を行う</span></label>
          <button type="submit">VPNログイン</button>
          {message && <div className="message">{message}</div>}
        </form>
      </section>
    </AppShell>
  );
}
