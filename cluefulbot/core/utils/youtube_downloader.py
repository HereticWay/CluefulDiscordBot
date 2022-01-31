from __future__ import unicode_literals
import typing as t
import yt_dlp

_last_filename = ""


def progress_hook(data):
    global _last_filename
    if len(_last_filename) == 0:
        _last_filename = data['filename']

    if data['status'] == 'finished':
        print('Done downloading, now converting ...')


def download_mp3(url: str) -> tuple[bool, str]:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
        'outtmpl': "./.cache/music/%(id)s.mp3",
    }

    global _last_filename
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download((url,))
            return True, _last_filename
    except Exception:  # TODO: implement proper error handling instead
        return False, ""
