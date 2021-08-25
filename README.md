## このシステムは？
某大学の学務情報システムで更新された成績を通知するものです。<br/>
GCPで自動デプロイを定期的に繰り返し、成績が更新されていればLINEで通知します。

## 使用技術
Python3.7.3<br/>
selenium<br/>
BeautifulSoup4<br/>
LINE Notify API<br/>
Chromedriver<br/>
Google Cloud Platform

### 導入方法
#### 1. LINE Notifyのアクセストークンを発行する
#### 2. Google Cloud Platformでプロジェクトを立てる。
#### 3. Google Cloud PlatformでCloud Shellを開き、このリポジトリをクローンする
#### 4. クラウド環境でライブラリをインストールする
#### 5. 環境変数でID・パスワード・アクセストークンを適応させる
#### 6. プログラムを自動デプロイを定期実行させて終了
