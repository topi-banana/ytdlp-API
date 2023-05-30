# yt-dlp API

これは、[yt-dlp](https://github.com/yt-dlp/yt-dlp)をWebAPIとして使えるようにしたものです

必要なパラメーターは、URLとDLTypeだけです

## Installation & Run

```sh
$ git clone https://github.com/topi-banana/ytdlp-API
$ cd ytdlp-API
```
### Docker (recommend)
run
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

default : **80**

APIの公開ポート

* `YTDLPAPI_HOST`

default : **0.0.0.0**

APIの公開IP
