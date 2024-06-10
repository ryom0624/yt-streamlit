from st_files_connection import FilesConnection
import streamlit as st
import yt_dlp

import os
import urllib.parse

# yt-dlpのオプション設定
ydl_opts = {
    'outtmpl': 'downloaded_video.mp4',
    'format': 'bestvideo[height=720][ext=mp4]+bestaudio[ext=m4a]/best[height=720][ext=mp4]',
    'merge_output_format': 'mp4',
    'nooverwrites': False,
}

# FilesConnectionを使用してGCSに接続
# conn = st.experimental_connection('gcs', type=FilesConnection)
conn = st.connection('gcs', type=FilesConnection)
gcs_bucket = "yt-download-streamlit"

st.title("YouTube動画ダウンロードアプリ")

# ユーザーからURLの入力を受け付ける
video_url = st.text_input("YouTubeの動画URLを入力してください:", placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX")

if st.button('ダウンロード開始'):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        res = ydl.extract_info(video_url, download=False)
        video_file_name = res['title']
        ydl.download([video_url])
        st.write(f"動画ID: {res['id']}")
        st.write(f"タイトル: {res['title']}")
        st.write(f"フォーマット: {res['format_note']}")
        st.write(f"投稿日時: {res['upload_date']}")
        st.write(f"投稿者: {res['uploader']}")
        st.write(f"再生回数: {res['view_count']}")
        # st.write(f"いいね数: {res['like_count']}")

        with open('downloaded_video.mp4', 'rb') as video_file:
            # ファイルをGCSに書き込む
            with conn.open(f"{gcs_bucket}/{video_file_name}.mp4", 'wb') as gcs_file:
                gcs_file.write(video_file.read())
                st.write("アップロード完了しました。")

        # ローカルのファイルを削除
        local_file_path = "downloaded_video.mp4"
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
            st.write(f"ローカルのファイル{local_file_path}を削除しました。")
        else:
            st.write("ファイルが存在しません。")


    encoded_url = urllib.parse.quote(video_file_name)
    download_url = f"https://storage.googleapis.com/{gcs_bucket}/{encoded_url}.mp4"

    # ダウンロードリンクを表示
    st.write(f"{video_file_name}がアップロードされました。")
    st.markdown(f"[ここをクリックしてダウンロード]({download_url})")
