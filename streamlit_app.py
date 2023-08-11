import streamlit as st
import yt_dlp
from st_files_connection import FilesConnection

# yt-dlpのオプション設定
ydl_opts = {
    'outtmpl': 'downloaded_video.mp4',
    'format': 'bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/best[height=720][ext=mp4]',
    'merge_output_format': 'mp4',
    'nooverwrites': False,
}

# ユーザーからURLの入力を受け付ける
video_url = st.text_input("YouTubeの動画URLを入力してください:")

# ボタンがクリックされたらダウンロード開始
if st.button('ダウンロード開始'):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(video_url, download=True)
        st.write(f"動画ID: {res['id']}")
        st.write(f"フォーマット: {res['format_note']}")

# FilesConnectionを使用してGCSに接続
conn = st.experimental_connection('gcs', type=FilesConnection)

# ダウンロードした動画ファイル名
video_file_name = "downloaded_video.mp4"

# ファイルをGCSに書き込む
with open(video_file_name, 'rb') as local_file:
    with conn.open(video_file_name, 'wb') as gcs_file:
        gcs_file.write(local_file.read())

st.write(f"{video_file_name}がGCSにアップロードされました。")
