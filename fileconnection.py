import streamlit as st
from st_files_connection import FilesConnection

# ファイル名
file_name = "text.txt"
file_content = "Hello, world!"
gcs_bucket = "yt-download-streamlit"

# Google Cloud Storageに接続
conn = st.experimental_connection('gcs', type=FilesConnection)

# ファイルが存在しない場合、新しく書き込む
try:
    _ = conn.read(f"{gcs_bucket}/{file_name}", input_format='text')
except FileNotFoundError:
    # ファイルを開く
    with conn.open(f"{gcs_bucket}/{file_name}", "wt") as f:
        # ファイルに書き込む
        f.write(file_content)

# 書き込んだ内容を確認
st.write(conn.read(f"{gcs_bucket}/{file_name}", input_format='text'))
