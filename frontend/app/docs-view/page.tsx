import { AppShell } from "../nav";

const flows = [
  ["1", "ユーザーが業務ダッシュボードへアクセスし、ログイン画面へ遷移"],
  ["2", "Mock SSOがユーザーID、パスワード、アカウント状態を確認"],
  ["3", "Mock MFAで6桁コードまたは承認ボタンを確認"],
  ["4", "認証ログをSQLiteに保存し、ダッシュボードへ遷移"],
  ["5", "管理画面でユーザー、アプリ、ポリシー、監査ログを確認"]
];

export default function DocsViewPage() {
  return (
    <AppShell>
      <div className="page-header"><div><h1 className="page-title">認証フロー説明</h1><p className="page-lead">SSO、MFA、VPN/RADIUS想定、監査ログの流れを日本語で整理します。</p></div></div>
      <section className="panel doc-flow">
        {flows.map(([no, text]) => <div className="flow-step" key={no}><strong>{no}. </strong>{text}</div>)}
      </section>
      <section className="panel">
        <h2>Duo OIDC連携想定</h2>
        <p>AUTH_MODE=duo_oidc、Client ID、Client Secret、Issuer、Redirect URIを.envに設定することで、OIDC連携検証へ拡張できる設計です。秘密情報はリポジトリに含めません。</p>
      </section>
    </AppShell>
  );
}
