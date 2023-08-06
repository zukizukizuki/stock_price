function myFunction() {
  // #行の変数
  i = 2

  // #スプシ,シートを取得
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName('2023年(投資家が勧めてた銘柄)');
  
  // 既に入ってる値を削除
  const clearrange = sheet.getRange("I2:I1000")
  clearrange.clearContent();

  // #空白までループ
  while (sheet.getRange(i, 3).getValue() != ""){
    const url = sheet.getRange(i, 4).getValue()
    const response = UrlFetchApp.fetch(url);
    const text = response.getContentText()
    
    const stock_price_all = Parser.data(text).from('<div class="YMlKec fxKbKc">').to("</div>").build()
    const stock_price = stock_price_all.replace("¥","")
    Logger.log(stock_price)
    sheet.getRange(i, 9).setValue(stock_price)
    i = i + 1
  }
  Browser.msgBox( "出力完了" )
}