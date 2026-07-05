import Link from "next/link";

const links = [
  ["/", "トップ"],
  ["/login", "ログイン"],
  ["/dashboard", "ダッシュボード"],
  ["/admin/users", "ユーザー管理"],
  ["/admin/applications", "アプリ管理"],
  ["/admin/policies", "ポリシー管理"],
  ["/admin/logs", "認証ログ"],
  ["/vpn-login", "VPNログイン"],
  ["/docs-view", "フロー説明"]
];

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="shell">
      <aside className="sidebar">
        <div className="brand">企業向けSSO/MFA<br />認証基盤ラボ</div>
        <nav className="nav">
          {links.map(([href, label]) => (
            <Link key={href} href={href}>{label}</Link>
          ))}
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
