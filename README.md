# mentemo logs

メンテモの**全案件**と**開発**を管理するリポジトリです。

## 構成

| フォルダ | 内容 |
|----------|------|
| **[ピッカーズ](./ピッカーズ/)** | 施策ログ・議事録・データ（Googleリスティング・サイト改善・Meta広告 等） |
| （今後） | 他案件・開発用フォルダを追加 |

## 運用

- 案件ごとにフォルダを分け、中で `施策ログ`（data / logs）や開発コードを管理
- 大事なデータのみ保存（メール文全文は保存しない方針）
- 日付は `YYYY-MM-DD` 形式

## GitHub

リポジトリ名: **mentemo logs**

```bash
cd ~/Desktop/AI
git remote add origin https://github.com/<ユーザー名>/mentemo-logs.git
git push -u origin main
```
