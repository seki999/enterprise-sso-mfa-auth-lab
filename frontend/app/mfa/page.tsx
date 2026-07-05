"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiPost } from "../../lib/api";

type LoginResponse = { success: boolean; message: string; token?: string; next_step?: string };

export default function MfaPage() {
  const router = useRouter();
  const [code, setCode] = useState("123456");
  const [message, setMessage] = useState("");

  async function verify(approve: boolean) {
    const token = localStorage.getItem("auth_lab_pending_token") ?? "";
    const result = await apiPost<LoginResponse>("/auth/mfa/verify", { token, code, approve });
    setMessage(result.message);
    if (result.success && result.token) {
      localStorage.setItem("auth_lab_token", result.token);
      localStorage.removeItem("auth_lab_pending_token");
      router.push("/dashboard");
    }
  }

  return (
    <div className="login-layout">
      <section className="panel login-panel">
        <h1 className="page-title">Mock MFA</h1>
        <p className="page-lead">6桁コードまたは承認ボタンでMFA成功を再現します。</p>
        <div className="form">
          <label>6桁コード<input value={code} onChange={(e) => setCode(e.target.value)} maxLength={6} /></label>
          <div className="actions">
            <button onClick={() => verify(false)}>コードで確認</button>
            <button className="secondary" onClick={() => verify(true)}>承認</button>
          </div>
          {message && <div className="message">{message}</div>}
        </div>
      </section>
    </div>
  );
}
