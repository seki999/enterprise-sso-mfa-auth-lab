"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiPost } from "../../lib/api";

type LoginResponse = { success: boolean; message: string; token?: string; next_step?: string };

export default function LoginPage() {
  const router = useRouter();
  const [userId, setUserId] = useState("employee01");
  const [password, setPassword] = useState("Password123!");
  const [message, setMessage] = useState("");

  async function submit(event: React.FormEvent) {
    event.preventDefault();
    const result = await apiPost<LoginResponse>("/auth/login", { user_id: userId, password });
    setMessage(result.message);
    if (result.success && result.token) {
      localStorage.setItem("auth_lab_pending_token", result.token);
      router.push("/mfa");
    }
  }

  return (
    <div className="login-layout">
      <section className="panel login-panel">
        <div className="page-header">
          <div>
            <h1 className="page-title">ログイン</h1>
            <p className="page-lead">Mock SSOでユーザーIDとパスワードを確認します。</p>
          </div>
        </div>
        <form className="form" onSubmit={submit}>
          <label>ユーザーID<input value={userId} onChange={(e) => setUserId(e.target.value)} /></label>
          <label>パスワード<input type="password" value={password} onChange={(e) => setPassword(e.target.value)} /></label>
          <button type="submit">SSOログイン</button>
          {message && <div className="message">{message}</div>}
        </form>
      </section>
    </div>
  );
}
