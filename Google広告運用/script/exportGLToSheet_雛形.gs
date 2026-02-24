/**
 * GL（Googleリスティング）→ スプシ 出力の雛形
 * 使い方: 下記の定数を差し替え、GAS（Google広告スクリプト）に貼って main を実行
 */
const STARTED_AT = '20251201';           // 集計開始日 YYYYMMDD
const CAMPAIGN_ID = 'LT00XXX';           // キャンペーンID（ssid_ltid_mapping.json の LTID）
const SPREADSHEET_ID = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';  // スプシのID
const SHEET_NAME = '_RAW_';             // 出力先シート名

function formatDate(date) {
  const d = new Date(date);
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const day = d.getDate().toString().padStart(2, '0');
  const year = d.getFullYear().toString();
  return year + month + day;
}

function main() {
  const endedAt = formatDate(new Date());

  const spreadsheet = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = spreadsheet.getSheetByName(SHEET_NAME);

  const query = `
    SELECT
      segments.date,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions
    FROM
      campaign
    WHERE
      segments.date BETWEEN ${STARTED_AT} AND ${endedAt}
      AND campaign.name LIKE "${CAMPAIGN_ID}%"
    ORDER BY segments.date ASC
  `;

  try {
    const report = AdsApp.report(query);
    report.exportToSheet(sheet);
    Logger.log('Report successfully exported to sheet.');
  } catch (error) {
    Logger.log('Failed to export report - ' + error.toString());
    throw error;
  }
}
