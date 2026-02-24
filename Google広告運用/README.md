# Google広告運用（会社共通）

**SSID/LTID・GL→スプシ** は**会社（メンテモ）の**仕組みです。ピッカーズと SSID のある案件は**並列**で、ここは会社共通の雛形・マスタの置き場です。

Google広告のキャンペーン別数値を **Googleスプレッドシート** に送る運用（GL→スプシ）の設定・雛形です。

## 構成

| ファイル／フォルダ | 内容 |
|--------------------|------|
| **config/ssid_ltid_mapping.json** | SSID（会社）・LTID（キャンペーン＝エリア＋商材）マスタ |
| **config/campaigns_sheets.json** | キャンペーンID・スプシID対応（南関東3キャンペーン等） |
| **config/会社別_sheet_雛形.json** | 会社別スプシ設定の雛形（コピーしてID・LTIDを埋める） |
| **config/清亀石油_sheet.json** | 清亀石油（朝霞・車検）用スプシ設定 |
| **script/exportGLToSheet_雛形.gs** | GL→スプシ1社用のGAS雛形（定数だけ差し替えて使う） |
| **script/exportCampaignReportToSheet.gs** | 複数キャンペーン一括出力（南関東用） |

## IDの意味

| ID | 対応 |
|----|------|
| **SSID** | 会社に対応（[SSID/](./SSID/) で会社別フォルダを管理） |
| **LTID** | リスティング広告のキャンペーン（エリア＋商材が紐付く） |

## 雛形の使い方（会社別 GL→スプシ）

1. **config/会社別_sheet_雛形.json** をコピーし、会社名・LTID・スプレッドシートID・エリア・商材を埋めて保存（例: `config/清亀石油_sheet.json`）。
2. **script/exportGLToSheet_雛形.gs** を開き、先頭の定数を同じ内容に差し替える。
3. Google広告のスクリプト画面に貼り付け、`main` を実行。

## 関連

- **ピッカーズ** … 例外で SSID/LTID を持たない。施策ログは [ピッカーズ/施策ログ](../ピッカーズ/施策ログ) で管理。
- **SSID別一覧** … [SSID/](../SSID/)
