# FishApp


### 概要
---
釣り日記を投稿できるwebアプリケーションです。  
投稿できる内容は釣り日記タイトル、本文、場所、釣れた魚名とその画像です。  
季節や地域によって釣れる魚も変わるため、新鮮な情報をネット上で共有することでターゲット決めなどに役立てることができます。

### 利用方法
ログインすることで釣り日記の投稿やユーザーのフォローやコメントの書き込みができるようになります。  
魚の名前と場所を指定して投稿の検索ができます。

### 目指した課題解決
- 釣り初心者に対して  
初心者は今の季節に地元でどのような魚が釣れているかや、どのような仕掛けを使ったらいいかわからないことが多いです。  
場所や時期や釣り方などの情報を多くのユーザーが成果とともに共有することで初心者でも釣りの方針が立てやすくなります。

- 全てのユーザーに対して  
個人で取り組むことが多い趣味であるため釣り人同士の情報交換の機会はあまり多くありません。  
他のユーザーの投稿を閲覧するだけでなくコメント欄やフォロー機能やメッセージ機能を活用することでより情報交換などしやすくしました。  

### 使用した技術
Python3 Django HTML Bootstrap4 JavaScript PostgreSQL Docker Github AWS(ECS, Fargate, S3, RDS)

### URL
http://fish-app-ee246f6eb5b2565b.elb.ap-northeast-1.amazonaws.com/trips/index/

### テスト用アカウント
メールアドレス: guest@guest.com  
パスワード: guestpass123


### インフラ構成図
![fargate4](https://user-images.githubusercontent.com/89190802/143770200-60591580-2cab-476e-a1e4-94a0491f3689.png) 

### 実装した機能のGIF
- トップページ  

![投稿一覧](https://user-images.githubusercontent.com/89190802/143769701-44ade03b-8b7f-4f4c-8b8b-c6df6300fc4b.jpeg)  
投稿が新着順に表示されます。  
見やすさのために写真は一枚だけ、文字数は先頭の65字まで表示されます。  
ページネーション機能を加えて1ページにつき6件まで表示されます。

---

- 投稿詳細ページ  

![投稿詳細](https://user-images.githubusercontent.com/89190802/143769871-199df0f3-d7ee-4a65-b8fc-f25cbdd78121.gif)
トップページでは省略されていた画像や本文も全て表示します。  ログイン中のユーザーはコメントの投稿と削除をすることができます。

---

- 新規投稿ページ  

![新規投稿](https://user-images.githubusercontent.com/89190802/143769900-101929a0-addc-43d8-8820-8bebb18706ad.gif)
フォームを埋めるだけで釣り日記を作成できます。  
釣れた魚の数に応じて釣果のフォームをAddボタンとDeleteボタンで増減できます。

---

- 投稿編集ページ  

<img width="1440" alt="投稿編集" src="https://user-images.githubusercontent.com/89190802/143769946-580ace54-ce2e-4639-a30e-5e2f47332c77.png">
フォームには投稿済みの情報が既に書き込まれた状態で表示されます。  
記入内容を書き換えた上で送信することで投稿の編集ができます。

---


- 投稿検索ページ  

<img width="1439" alt="検索" src="https://user-images.githubusercontent.com/89190802/143770050-b1f6bad7-272c-404c-a021-3ff82b8d89cc.png">
魚名と場所(都道府県)を指定して釣果を検索することができます。  
条件にヒットする投稿の数を月別でグラフに表示します。季節による釣れ方の違いが分かりやすくなります。

---

- 投稿履歴  

![マイページ](https://user-images.githubusercontent.com/89190802/143770073-e1ab2c28-c3d7-4bc6-9999-0c300726b963.jpeg)
ユーザーの投稿履歴と自己紹介文が表示されます。

---

- フォローリストページ  

![フォローリスト](https://user-images.githubusercontent.com/89190802/145308560-d7d8b888-d426-4536-bc1d-d12b32c7583a.gif)
ユーザーのフォロー状況が表示されます。ログイン状態でフォローすることができます。  
相互フォロー状態でメッセージボタンが表示されます。

---

- メッセージページ  

<img width="1440" alt="fish_message" src="https://user-images.githubusercontent.com/89190802/145308086-268fe3fa-940f-428b-9527-1cc9f7a42061.png">
相互フォロー状態でフォロワー同士でメッセージの交換ができます。　　
少なくとも一方のフォローが外れた時はメッセージフォームは非表示になり過去の履歴の閲覧のみ可能になります。

---

- ログイン  

<img width="1440" alt="ログイン" src="https://user-images.githubusercontent.com/89190802/143770075-415a1a8e-7a2b-4055-a3bd-99450252a531.png">
メールアドレスとパスワードでログインできます。  

---

- 新規登録  

<img width="1439" alt="新規登録" src="https://user-images.githubusercontent.com/89190802/143770102-26856eb8-c75d-4d80-9320-edabac9437d2.png">
新規のユーザー登録ページです。  

---

- ユーザー編集ページ  

<img width="1440" alt="ユーザー編集" src="https://user-images.githubusercontent.com/89190802/143770110-26d9828a-1d51-4159-be97-8bc01f495166.png">
ユーザー名と自己紹介文を編集できます。  

---

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
