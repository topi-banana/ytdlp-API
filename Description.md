# Description

これは、[yt-dlp](https://github.com/yt-dlp/yt-dlp)をWebAPIとして使えるようにしたものです

必要なパラメーターは、URLとDLTypeだけです

# Parameter

## URL: str

```
https://youtube.com/watch?v=xxxxxxxx
http://youtu.be/xxxxxxxx
```

上記のような文字列です

これはYoutubeに限らず、[yt-dlpのサポートしているサイト](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)なら何でも可能です。

※すべてのサイトを検証して公開しているわけではないので一部不具合が生じるものがある可能性があります。

## DLType: ['video' or 'audio']

`Download Type`です
`video`と`audio`から選択可能で、どちらも`format:best`です

それ以外は選択不可です

## ID :str

Downloadを要求したときに帰ってくるIDで、そのプロセスを見るときだけ必要です