import re

import click
from rich import print

from requests import get as request

class URL(str):
  def __init__(self, txt:str):
    if not re.search(r'^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+$',txt):
      raise TypeError(f'Malformed URL : "{txt}"')
    self = txt

@click.command()
@click.option('-u', '--url', help='URL')
@click.option('-p', '--proccess-id', help='プロセスID')
@click.option('-h', '--host', help='APIのホスト', show_default=True, default='127.0.0.1:10487')
@click.option('-a', '--audio', help='ダウンロードタイプをaudioに変更する', is_flag=True)
@click.option('-i', '--info', help='動画の情報の表示', is_flag=True)
@click.option('--dev', is_flag=True)
def main(url:str, proccess_id:str, host:str='127.0.0.1:10487', audio:bool=False, info:bool=False, dev:bool=False):
  if dev:
    print(url)
    print(proccess_id)
    print(host)
    print(audio)
    print(info)
  if info:
    if not url:
      url = input('URL : ')
    res = request(f"http://{host}/info", params={
      'url': url,
    })
  elif proccess_id:
    res = request(f"http://{host}/proccess/{proccess_id}")
  else:
    if not url:
      url = input('URL : ')
    res = request(f"http://{host}/dl/{'audio' if audio else 'video'}", params={
      'url': url,
    })
  print(res.json())

#request(args.url)



if __name__ == '__main__':
  main()