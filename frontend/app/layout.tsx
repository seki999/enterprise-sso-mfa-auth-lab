import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "企業向けSSO/MFA認証基盤ラボ",
  description: "Mock SSO/MFAとDuo OIDC連携想定を確認する学習・検証用サンプル"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
