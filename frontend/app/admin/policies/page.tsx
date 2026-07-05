"use client";

import { useEffect, useState } from "react";
import { AppShell } from "../../nav";
import { apiGet } from "../../../lib/api";

type Policy = { id: number; name: string; condition: string; action: string; priority: number };

export default function PoliciesPage() {
  const [policies, setPolicies] = useState<Policy[]>([]);
  useEffect(() => { apiGet<Policy[]>("/policies").then(setPolicies); }, []);
  return (
    <AppShell>
      <div className="page-header"><div><h1 className="page-title">ポリシー管理</h1><p className="page-lead">本番環境では、ユーザーグループ、端末状態、IPアドレス、アプリケーション単位でポリシーを設計します。</p></div></div>
      <section className="panel table-wrap">
        <table><thead><tr><th>優先度</th><th>ポリシー</th><th>条件</th><th>アクション</th></tr></thead>
          <tbody>{policies.map((policy) => <tr key={policy.id}><td>{policy.priority}</td><td>{policy.name}</td><td>{policy.condition}</td><td>{policy.action}</td></tr>)}</tbody></table>
      </section>
    </AppShell>
  );
}
