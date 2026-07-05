# 07_Duo連携想定メモ

## Cisco Duo Trial / Free を利用した検証観点

OIDCアプリ作成、Redirect URI登録、ユーザー登録、MFA方式、ログ確認を行います。

## Duo OIDC連携の確認項目

Client ID、Client Secret、Issuer、Redirect URI、スコープ、時刻同期、証明書を確認します。

## Duo Mobile MFAの確認項目

Push到達、承認、拒否、端末紛失時、再登録、バックアップコード相当の運用を確認します。

## Authentication Proxy / RADIUS / LDAP / AD 連携の想定

VPN装置からRADIUS要求を受け、LDAP/ADで一次認証し、MFA承認後にAccess-Acceptを返す構成を想定します。

## 実案件で確認すべき質問リスト

対象ユーザー数、対象アプリ、管理者範囲、社外アクセス条件、既存IdP、AD構成、監査要件、障害時連絡先、運用体制を確認します。

## 設計・構築フェーズで作成する成果物

基本設計書、詳細設計書、構築手順書、試験仕様書、運用手順書、障害調査手順書、認証ログ確認手順を作成します。
