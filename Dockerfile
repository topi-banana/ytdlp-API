FROM python

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install \
#  fastapi uvicorn[standard] yt-dlp
  -r requirements.txt

RUN cd /;\
  curl -O https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz;\
  tar -xf ffmpeg-release-amd64-static.tar.xz;\
  rm -rf ffmpeg-release-amd64-static.tar.xz;\
  export PATH=/ffmpeg-4.2.3-amd64-static:$PATH;

EXPOSE 10487

ENV YTDLPAPI_MAX_PROC=1
ENV YTDLPAPI_TMP_DIR=/tmp
ENV YTDLPAPI_PORT=10487
ENV YTDLPAPI_HOST=0.0.0.0
ENV YTDLPAPI_KEEP_TIME=255

COPY ./ ./

CMD ["python", "main.py"]