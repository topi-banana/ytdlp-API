# yt-dlp API

これは、[yt-dlp](https://github.com/yt-dlp/yt-dlp)をWebAPIとして使えるようにしたものです

必要なパラメーターは、URLとDLTypeだけです

## Installation & Run

```sh
$ git clone https://github.com/topi-banana/ytdlp-API
$ cd ytdlp-API
```
### Docker (recommend)
```
$ docker build . -t ytdlp-api
```
#### docker run
```sh
$ docker run ytdlp-api
```
Optional
```sh
$ docker run \
  -e YTDLPAPI_MAX_PROC=10 \
  -e YTDLPAPI_KEEP_TIME=25 \
  -p 8080:80 \
  -v tmp:/tmp \
  ytdlp-api
```
#### docker compose
```sh
$ docker compose up
```
### Local
install
```sh
$ pip install -r requirements.txt
# or
$ pip install yt-dlp fastapi uvicorn[standard]
```
run
```sh
$ python main.py
```
## Document
### Parameter

* `URL`: `str`

```
https://youtube.com/watch?v=xxxxxxxx
http://youtu.be/xxxxxxxx
```

上記のような文字列です

これはYoutubeに限らず、[yt-dlpのサポートしているサイト](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)なら何でも可能です。

※すべてのサイトを検証して公開しているわけではないので一部不具合が生じるものがある可能性があります。

* `DLType`: [`video` or `audio`]

`Download Type`です
`video`と`audio`から選択可能で、どちらも`format:best`です

それ以外は選択不可です

* `ID` :`str`

Downloadを要求したときに帰ってくるIDで、そのプロセスを見るときだけ必要です


### ENV

* `YTDLPAPI_KEEP_TIME`

default : **255** (sec)

プロセス終了後にそのプロセスを保持する時間

* `YTDLPAPI_MAX_PROC`

default : **1**

ダウンロードプロセスの同時に実行できる最大数

* `YTDLPAPI_TMP_DIR`

default : **/tmp**

ダウンロードしたファイルの保存場所

* `YTDLPAPI_PORT`

default : **10487**

APIの公開ポート

* `YTDLPAPI_HOST`

default : **0.0.0.0**

APIの公開IP

# CLI client

`requests.get` と `rich` を使ってAPIアクセスを少し簡単にしただけのクソ雑クライアント

引数パーサーには`click`を使用

（今後修正予定）
## How to use
```sh
$ python client.py --help
```
```
Usage: client.py [OPTIONS]

Options:
  -u, --url TEXT          URL
  -p, --proccess-id TEXT  プロセスID
  -h, --host TEXT         APIのホスト  [default: 127.0.0.1:10487]
  -a, --audio             ダウンロードタイプをaudioに変更する
  -i, --info              動画の情報の表示
  --help                  Show this message and exit.
```

# Change log

* 0.1.0 (2023/6/2)
  
  [CLI クライアント(クソ雑)]()

  デフォルトポートの変更 80 -> 10487

* 0.0.1 (2023/5/31)
  
  [API部分の完成](https://github.com/topi-banana/ytdlp-API/commit/34ed8c54a19b9db5e19b64426d7924e56be783c2)