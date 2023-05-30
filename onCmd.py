import yt_dlp
from typing import Literal
from threading import Thread

URL = input()
dltype = 'video'
def main():
  #URL:str = 'https://tver.jp/episodes/epr9vrvsyx'
  #dltype:Literal['video','audio'] = 'video'
  with yt_dlp.YoutubeDL({}) as ydl:
    info = ydl.extract_info(URL, download=False)
  class MyLogger:
    def debug(self, msg):
      pass
    def info(self, msg):
      pass
    def warning(self, msg):
      pass
    def error(self, msg):
      print(msg)
  def my_hook(d):
    if d['status'] == 'finished':
      print('Done downloading, now post-processing ...')
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
    'progress_hooks': [my_hook],
    'logger': MyLogger(),
    'outtmpl': f"./tmp/{info['id']}.%(ext)s",
  }
  with yt_dlp.YoutubeDL({**ydl_opts,**default}) as ydl:
    ydl.download(URL)

#main()
t = Thread(target=main)
t.start()
print("this will be printed immediately")

t.join()


print("this will be printed immediately")
