/**
 * ピッカーズ Google広告：キャンペーン別数値をスプレッドシートへ出力
 * 運用: campaigns_sheets.json のキャンペーン・シートIDに対応
 */
const startedAt = '20251201';
const campaigns = ['LT00175', 'LT00176', 'LT00177'];
const sheetName = '_RAW_';
const sheetIds = {
  'LT00175': '1pQ4FlTW0s8Df2kvp4PUr5sr39PMCKwPuKdtrmpD5CR0',
  'LT00176': '1KuOFlL8KGS-c1CJF78gC5z4jiZOsYsaa9Clo9av31Qw',
  'LT00177': '1LoMxh920x_92aS71njG75f1ghxLVjqK5iMoSdIicOVg'
};

function formatDate(date) {
  const d = new Date(date);
  const month = (d.getMonth() + 1).toString().padStart(2, '0');
  const day = d.getDate().toString().padStart(2, '0');
  const year = d.getFullYear().toString();
  return year + month + day;
}

function main() {
  const endedAt = formatDate(new Date());

  for (const campaign of campaigns) {
    console.log(sheetIds[campaign]);
    const spreadsheet = SpreadsheetApp.openById(sheetIds[campaign]);
    const sheet = spreadsheet.getSheetByName(sheetName);
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
          segments.date BETWEEN ${startedAt} AND ${endedAt}
          AND campaign.name LIKE "${campaign}%"
         ORDER BY segments.date ASC
    `;

    try {
      const report = AdsApp.report(query);
      report.exportToSheet(sheet);
      Logger.log('Report successfully exported.');
    } catch (error) {
      Logger.log('Failed to export report: ' + error.toString());
    }
  }
}
