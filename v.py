#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Streamlit App : YouTube → MP4 Converter
Dépendances : streamlit, yt-dlp, ffmpeg
Installation :
  pip install streamlit yt-dlp
  # ffmpeg doit être dans le PATH
  # Windows : ajoutez le dossier bin de ffmpeg à votre PATH
  # macOS (Homebrew) : brew install ffmpeg
  # Debian/Ubuntu : sudo apt install ffmpeg

Lancez : streamlit run yt_to_mp4_streamlit.py
"""

import os
import tempfile

import streamlit as st
from yt_dlp import YoutubeDL

def download_youtube_mp4(
    url: str,
    output_dir: str,
    filename: str = None
) -> str:
    """
    Télécharge la meilleure version MP4 (audio+vidéo fusionnés)
    et la sauve sous output_dir/[filename or title].mp4
    """
    os.makedirs(output_dir, exist_ok=True)
    tmpl = os.path.join(output_dir, filename or "%(title)s") + ".%(ext)s"

    ydl_opts = {
        "format":    "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "merge_output_format": "mp4",
        "outtmpl":   tmpl,
        "noplaylist": True,
        "quiet":     True,
        "no_warnings": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "video")
        fname = f"{filename or title}.mp4"
        return os.path.join(output_dir, fname)

# ─── Streamlit UI ──────────────────────────────────────────────────────────────

st.set_page_config(page_title="YouTube → MP4", layout="centered")
st.title("📥 YouTube → MP4 Converter")

url_input      = st.text_input("🔗 URL de la vidéo YouTube")
filename_input = st.text_input("✏️ Nom de fichier (sans extension, facultatif)")

if st.button("🚀 Télécharger & Convertir"):
    if not url_input.strip():
        st.error("✋ Merci d'entrer une URL valide.")
    else:
        with st.spinner("⏳ Traitement en cours…"):
            try:
                # création d'un dossier temp pour stocker le MP4
                tmp_dir = tempfile.mkdtemp(prefix="ytmp4_")
                mp4_path = download_youtube_mp4(url_input.strip(), tmp_dir, filename_input.strip() or None)

                st.success(f"✅ Vidéo enregistrée : `{os.path.basename(mp4_path)}`")
                # Affiche un aperçu si possible
                st.video(mp4_path)

                # Bouton pour télécharger
                with open(mp4_path, "rb") as f:
                    video_bytes = f.read()
                    st.download_button(
                        label="⬇️ Télécharger le MP4",
                        data=video_bytes,
                        file_name=os.path.basename(mp4_path),
                        mime="video/mp4"
                    )
            except Exception as e:
                st.error(f"❌ Une erreur est survenue :\n{e}")
