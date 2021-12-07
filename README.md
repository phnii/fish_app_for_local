# fish_app_for_local  
こちらはfish_appのローカルでの動作確認用のアプリです。fish_appのコードとの違いは投稿画像のアップロード先をS3のバケットにするか、Djangoアプリのディレクトリ内にするかの違いです。  
本番環境用のソースコードはこちらです↓  
https://github.com/phnii/fish_app  

### ローカルでの動作方法
こちらのローカル用のリポジトリからgit cloneします。
```
git clone https://github.com/phnii/fish_app_for_local.git
```
docker-compose.ymlファイルがあるディレクトリの中で次のコマンドを実行しコンテナを立ち上げます。
```
docker-compose up --build -d
```
djangoのマイグレーションファイルの作成。　　
DBの初期化に時間がかかってDBの接続に失敗することがあります。
その場合5~10秒ほど時間を置いてから再度下記のコマンドを実行してください。
```
docker-compose exec app python manage.py makemigrations
```
マイグレーションの実行。
```
docker-compose exec app python manage.py migrate
```
ブラウザからlocalhost/trips/indexにアクセスすることでトップページにアクセスできます。  
新規ユーザー作成時のメールアドレスはダミーのもので構いません。  
動作を確認終了したらコンテナを終了後しクローンしたディレクトリ、イメージ(fish_app_for_local_nginx, fish_app_for_local_app)、ボリューム(fish_app_for_local_tmp-data)を削除してください。
