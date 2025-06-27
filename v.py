#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App : YouTube → MP4 / MP3 Converter
Dépendances : streamlit, yt-dlp, ffmpeg
Installation :
  pip install streamlit yt-dlp
  # ffmpeg doit être dans le PATH
"""

import os
import tempfile
import streamlit as st
from yt_dlp import YoutubeDL

def download_youtube_mp4(url: str, output_dir: str, filename: str = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    tmpl = os.path.join(output_dir, (filename or "%(title)s")) + ".%(ext)s"
    ydl_opts = {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "merge_output_format": "mp4",
        "outtmpl": tmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        return os.path.join(output_dir, f"{filename or title}.mp4")

def download_youtube_mp3(url: str, output_dir: str, filename: str = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    tmpl = os.path.join(output_dir, (filename or "%(title)s")) + ".%(ext)s"
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": tmpl,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "audio")
        return os.path.join(output_dir, f"{filename or title}.mp3")

# ─── Streamlit UI ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="YouTube Downloader", layout="centered")
st.title("📥 YouTube Downloader")

# 1) Entrées
url_input      = st.text_input("🔗 URL de la vidéo YouTube")
mode           = st.radio("👉 Que voulez-vous télécharger ?", ["Vidéo (MP4)", "Audio (MP3)"])
filename_input = st.text_input("✏️ Nom de fichier (sans extension) – facultatif")

# 2) Bouton Go
if st.button("🚀 Démarrer"):
    if not url_input.strip():
        st.error("Merci d'entrer une URL valide.")
    else:
        with st.spinner("⏳ Traitement en cours…"):
            try:
                tmp_dir = tempfile.mkdtemp(prefix="yt_")
                if mode.startswith("Vidéo"):
                    out_path = download_youtube_mp4(
                        url_input.strip(), tmp_dir, filename_input.strip() or None
                    )
                    st.success(f"✅ MP4 prêt : {os.path.basename(out_path)}")
                    st.video(out_path)
                    data = open(out_path, "rb").read()
                    st.download_button("⬇️ Télécharger le MP4", data, os.path.basename(out_path), "video/mp4")
                else:
                    out_path = download_youtube_mp3(
                        url_input.strip(), tmp_dir, filename_input.strip() or None
                    )
                    st.success(f"✅ MP3 prêt  : {os.path.basename(out_path)}")
                    st.audio(out_path, format="audio/mp3")
                    data = open(out_path, "rb").read()
                    st.download_button("⬇️ Télécharger le MP3", data, os.path.basename(out_path), "audio/mp3")

            except Exception as e:
                st.error(f"❌ Une erreur est survenue :\n{e}")
