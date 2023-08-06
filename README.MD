# stock_price

### Description
- スプシにまとめた銘柄コードを読み込んで株価を取得します
- GASとPythonがあります
- 公開したくない情報はAWSの環境変数に組み込みます
- (予定) SNSからlambdaにpushしてPythonを動かす仕組みにしたい
- (予定) 気が向いたらCI/CD組むか aws-terraform リポジトリに組み込む

### Directory Layout

```
stock_price
│  backend.tf
│  README.MD
│
├─GAS
│      stock_price.gs
│
└─src
        main.py
        requirements.txt
```