# Google広告運用（ピッカーズ）

Google広告のキャンペーン別数値を **Googleスプレッドシート** に送る運用です。

## 構成

| ファイル／フォルダ | 内容 |
|--------------------|------|
| **config/campaigns_sheets.json** | キャンペーンID・スプレッドシートIDの対応（南関東3キャンペーン） |
| **config/会社別_sheet_雛形.json** | 会社別スプシ設定の雛形（コピーしてID・LTIDを埋める） |
| **script/exportGLToSheet_雛形.gs** | GL→スプシ1社用のGAS雛形（定数だけ差し替えて使う） |
| **script/exportCampaignReportToSheet.gs** | 複数キャンペーン一括出力（南関東用） |

## IDの意味

| ID | 対応 |
|----|------|
| **SSID** | 会社に対応 |
| **LTID** | リスティング広告のキャンペーン（エリア＋商材が紐付く） |

マスタ一覧: **config/ssid_ltid_mapping.json**

## スプシ連携キャンペーン（ピッカーズ運用）

- **LT00175** 園生（コーティング）… 出光リテール販売 南関東カンパニー
- **LT00176** 佐倉（コーティング）
- **LT00177** 市原（コーティング）

レポート項目: `segments.date`, `impressions`, `clicks`, `cost_micros`, `conversions`（シート名 `_RAW_`）。

## 雛形の使い方（会社別 GL→スプシ）

1. **config/会社別_sheet_雛形.json** をコピーし、会社名・LTID・スプレッドシートID・エリア・商材を埋めて保存（例: `config/清亀石油_sheet.json`）。
2. **script/exportGLToSheet_雛形.gs** を開き、先頭の定数（`CAMPAIGN_ID`, `SPREADSHEET_ID`, `STARTED_AT`, `SHEET_NAME`）を同じ内容に差し替える。
3. Google広告のスクリプト画面に貼り付け、`main` を実行。

## 関連

- 案件全体の予算・施策: `施策ログ/data/ピッカーズ案件_構造.json`（Googleリスティング 予算250万）
