# coding: UTF-8
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup
import requests
import time
import slackweb

# 例外発生通知用のslackのurl
SLACKURL_ex = ''

# main処理
def main():

    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    #jsonファイルを指定
    credentials = ServiceAccountCredentials.from_json_keyfile_name('jsonファイルパス', scope)

    # 認証
    gc = gspread.authorize(credentials)

    # 対象銘柄コード読み取り
    code_list = readSpreadsheet(gc)
    print(code_list)

    # 書き込み対象リスト定義
    price_list = []

    for i in range(1, len(code_list)):

        # スクレイピング対象URL
        URL = 'https://kabutan.jp/stock/?code=' + code_list[i]

        # スクレイピング実行
        try:
            #対象URLにリクエスト
            req = requests.get(URL)
            time.sleep(3)

            # 文字コードをUTF-8に変換し、html取得
            soup = BeautifulSoup(req.text, 'html.parser')

            # tagとclassを指定して要素を取り出す
            stock_price = soup.find('div', id='stockinfo_i1').find('span', class_='kabuka').text
            price_list.append(stock_price.replace('円',''))

        except Exception as e:
            message = "[例外発生]stock-price\n"+"type:{0}".format(type(e))+"\n"+"args:{0}".format(e.args)
            slackweb.Slack(url = SLACKURL_ex).notify(text = message)
            break

    print(price_list)
    # スプレッドシートへ株価を書き込む
    writeSpreadsheet(gc, price_list)
    slackweb.Slack(url = SLACKURL_ex).notify(text = "[完了通知]stock-priceの実行が完了しました")

def readSpreadsheet(gc):
    # 読み込むシートを指定
    target_sheet = gc.open('配当利回り基準_株買い時').worksheet('2023年(投資家が勧めてた銘柄)')
    # 指定した列のセルの値を読み込む
    value_list = target_sheet.col_values(2)
    return value_list


def writeSpreadsheet(gc, value_list):
    # 書き込み対象のシートを指定
    target_sheet = gc.open('配当利回り基準_株買い時').worksheet('2023年(投資家が勧めてた銘柄)')
    for i in range(0,len(value_list)):
        #対象のセルに値を書き込む(row, col, value)
        target_sheet.update_cell(i+2, 9, value_list[i])
        time.sleep(3)

if __name__ == '__main__':
    main()
