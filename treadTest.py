import yt_dlp
from typing import Literal
from threading import Thread
import json
import sys

def info(url:str):
  with yt_dlp.YoutubeDL({}) as ydl:
    dic = ydl.extract_info(url, download=False)
  del dic['formats'], dic['thumbnails'], dic['_format_sort_fields'], dic['requested_formats']
  return dic
def main(url:str, dltype:Literal['video','audio'] = 'video'):
  dic = info(url)
  class Logger:
    @staticmethod
    def debug(msg):
      pass
    @staticmethod
    def info(msg):
      pass
    @staticmethod
    def warning(msg):
      pass
    @staticmethod
    def error(msg):
      pass
  def hook(d):
    if 'filename'             in d: del d['filename']
    if 'formats'              in d['info_dict']: del d['info_dict']['formats']
    if 'thumbnails'           in d['info_dict']: del d['info_dict']['thumbnails']
    if '_format_sort_fields'  in d['info_dict']: del d['info_dict']['_format_sort_fields']
    if 'automatic_captions'   in d['info_dict']: del d['info_dict']['automatic_captions']
    if '_filename'            in d['info_dict']: del d['info_dict']['_filename']
    if 'http_headers'         in d['info_dict']: del d['info_dict']['http_headers']
    with open('hook.json', 'w', encoding='utf-8') as f:
      json.dump(d, f, indent=2, ensure_ascii=False)
    sys.exit()
    #statuses.add(d['status'])
    #if d['status'] == 'finished':
    #  print('Done downloading, now post-processing ...')
  ydl_opts:dict = {
    'format': 'b',
    'final_ext': 'mp4'
  } if dltype == 'video' else {
    'format': 'ba',
    'final_ext': 'mp3',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
    }]
  }
  default:dict = {
    'concurrent_fragment_downloads': 10,
    'cachedir': False,
    'progress_hooks': [hook],
    'logger': Logger(),
    'outtmpl': f"./tmp/{dic['id']}.%(ext)s",
  }
  with yt_dlp.YoutubeDL({**ydl_opts,**default}) as ydl:
    ydl.download(url)
  print('Fin')

#main()
try:
  while True:
    print("入力待ち")
    # スレッドの定義
    t = Thread(target=main,args=(input(),))
    # スレッドの開始
    t.start()
    print("スレッドの開始")
except KeyboardInterrupt:
  print("KeyboardInterrupt")

# スレッドが終了するまで街状態にする
#t.join()