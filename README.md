## Boiled Pork


### 予測モデルの作成

```
$ cd learning
$ mkdir -p ./models
$ python predict.py
```

### 予測データの登録
```
$ cd learning
$ python regist.py
```
### セットアップ

```
$ cd backend
$ bundle install --path vendor/bundle
$ bundle exec rake db:create
$ bundle exec rake db:migrate
$ bundle exec rake db:seed
$ bundle exec rails runner Tasks::ImportPast.execute
$ bundle exec rails s
```

```
$ cd frontend
$ react-native run-ios
```
