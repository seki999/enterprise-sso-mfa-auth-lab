import Link from "next/link";
import { AppShell } from "./nav";

export default function Home() {
  return (
    <AppShell>
      <div className="page-header">
        <div>
          <h1 className="page-title">企業向けSSO/MFA認証基盤ラボ</h1>
          <p className="page-lead">Cisco Duo等のMFA/SSO製品導入を想定した、学習・検証用の架空社内業務システムです。</p>
        </div>
        <Link className="button" href="/login">検証を開始</Link>
      </div>
      <div className="grid cols-3">
        <section className="panel">
          <div className="metric">認証方式</div>
          <div className="metric-value">Mock SSO / OIDC想定</div>
          <p>未設定時はMock認証で動作し、Duo OIDC設定を追加した場合の接続口を確認できます。</p>
        </section>
        <section className="panel">
          <div className="metric">MFA方式</div>
          <div className="metric-value">6桁コード / 承認</div>
          <p>検証用コードは <strong>123456</strong> です。承認ボタンでもMFA成功を再現できます。</p>
        </section>
        <section className="panel">
          <div className="metric">監査</div>
          <div className="metric-value">SQLiteログ保存</div>
          <p>成功、失敗、拒否、ロックを含む認証ログを保存し、管理画面で確認できます。</p>
        </section>
      </div>
    </AppShell>
  );
}
