import yt_dlp

from fastapi import FastAPI, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Literal
import uvicorn

from threading import Thread

import signal
import time
import os
import sys

with open('Description.md','r') as f:
  description = f.read()

app = FastAPI(
  title='yt-dlp API',
  description=description,
  version='0.0.1',
  terms_of_service='https://api.topi.cf/terms/',
  contact={
    'name': 'とぴ。',
    'url': 'https://twitter.com/topi_banana',
    'email': 'support@topi.cf',
  }
)

maxProc = int(os.environ['YTDLPAPI_MAX_PROC'])
tmpDir = os.environ['YTDLPAPI_TMP_DIR']

procs = dict()

app.mount('/files', StaticFiles(directory=tmpDir), name='static')

@app.get('/info')
def info(url:str):
  try:
    with yt_dlp.YoutubeDL({}) as ydl:
      dic = ydl.extract_info(url, download=False)
    del dic['formats'], dic['thumbnails'], dic['_format_sort_fields'], dic['requested_formats'], dic['subtitles']
  except yt_dlp.utils.DownloadError as e:
    return {'status':'error', 'detail': e}
  return {'status':'success', 'content':dic}

@app.get('/dl/{dltype}')
def download(url:str, dltype:Literal['video','audio']):
  dic = info(url)
  if dic['status'] != 'success':
    return
  dic = dic['content']
  if procs.get(dic['id']):
    # 既にプロセスが存在する
    return
  if len(procs) >= maxProc:
    # プロセス枠がすべて埋まってる
    return
  # スレッドの定義
  t = Thread(target=main,args=(url, dic, dltype))
  # スレッドの開始
  t.start()
  return {'status':'success', 'content': {'id':dic['id']}}

@app.get('/proccess/{id}')
def proccess(id:str):
  if procs.get(id):
    d = procs[id]
    if 'filename' in d:
      d['filename'] = os.path.join('/files', os.path.basename(d['filename']))
    if 'info_dict' in d:
      dic = d['info_dict']
      if 'formats'              in dic: del dic['formats']
      if 'subtitles'            in dic: del dic['subtitles']
      if 'thumbnails'           in dic: del dic['thumbnails']
      if '_format_sort_fields'  in dic: del dic['_format_sort_fields']
      if 'automatic_captions'   in dic: del dic['automatic_captions']
      if '_filename'            in dic: del dic['_filename']
      if 'http_headers'         in dic: del dic['http_headers']
    return {'status':'success', 'content': {'id':id, **d}}
  else:
    return {'status':'error', 'detail': f'not found proccess : {id}'}

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
  procs[d['info_dict']['id']] = d

def main(url:str, dic:dict, dltype:Literal['video','audio'] = 'video'):
  # プロセスの追加
  procs[dic['id']] = {'status':'start'}
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
    'outtmpl': f'''{tmpDir}/{dic['id']}.%(ext)s''',
    'ffmpeg_location': './ffmpeg'
  }
  with yt_dlp.YoutubeDL({**ydl_opts,**default}) as ydl:
    ydl.download(url)
  # プロセスを「完了」にする
  procs[dic['id']]['status'] = 'complete'
  # KEEP_TIME秒間プロセスの「完了」を示す状態を保持する
  time.sleep(int(os.environ['YTDLPAPI_KEEP_TIME']))
  # プロセスの削除
  del procs[dic['id']]


def SIGINT_handler(signal, frame):
  print(" SIGINT ")
  sys.exit()

signal.signal(signal.SIGINT, SIGINT_handler)

if __name__ == '__main__':
  uvicorn.run(app, host=os.environ['YTDLPAPI_HOST'], port=int(os.environ['YTDLPAPI_PORT']))