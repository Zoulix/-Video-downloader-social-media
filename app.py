import streamlit as st
import yt_dlp
import os
import re
import tempfile
import glob
import io

# ─── Config ────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="VidFetch", page_icon="⬇️", layout="centered")

MAX_SIZE_MB = 800

st.markdown("""
<style>
    .block-container { max-width: 680px; padding-top: 2rem; }
    .info-box {
        background: #f8f8f8;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        border: 1px solid #eee;
    }
    .title-text { font-weight: 700; font-size: 1.05rem; }
    .meta-text  { color: #666; font-size: 0.85rem; margin-top: 4px; }
    .warn-box {
        background: #fff8e1;
        border-left: 3px solid #f59e0b;
        padding: 0.7rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        color: #78350f;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Header ────────────────────────────────────────────────────────────────────
st.title("⬇️ VidDownloader")
st.caption("YouTube · Facebook · TikTok · Instagram · Twitter/X — sans pub.")
st.markdown(
    '<div class="warn-box">⚠️ Limite recommandée : vidéos sous <strong>800 MB</strong>.</div>',
    unsafe_allow_html=True,
)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def fmt_duration(sec):
    if not sec: return ""
    m, s = divmod(int(sec), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s" if h else f"{m}m {s}s"

def fmt_views(n):
    if not n: return ""
    if n >= 1_000_000: return f"{n/1_000_000:.1f}M vues"
    if n >= 1_000:     return f"{n/1_000:.0f}K vues"
    return f"{n} vues"

def clean_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', str(text))

def cleanup_tempdir(tmpdir):
    if tmpdir and os.path.exists(tmpdir):
        for f in glob.glob(os.path.join(tmpdir, "*")):
            try: os.remove(f)
            except Exception: pass
        try: os.rmdir(tmpdir)
        except Exception: pass

def get_mime(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return {
        ".mp4":  "video/mp4",
        ".mp3":  "audio/mpeg",
        ".m4a":  "audio/mp4",
        ".webm": "video/webm",
        ".mkv":  "video/x-matroska",
    }.get(ext, "application/octet-stream")

def build_ydl_opts(fmt_choice, quality_val, out_dir):
    opts = {
        "outtmpl":     os.path.join(out_dir, "%(title)s.%(ext)s"),
        "quiet":       True,
        "no_warnings": True,
    }
    q = quality_val

    if "MP3" in fmt_choice:
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    elif "M4A" in fmt_choice:
        opts["format"] = "bestaudio[ext=m4a]/bestaudio/best"
    elif "WebM" in fmt_choice:
        h = "" if q == "best" else f"[height<={q}]"
        opts["format"] = f"bestvideo{h}[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best"
    else:  # MP4
        opts["format"] = (
            "bestvideo+bestaudio/best" if q == "best"
            else f"bestvideo[height<={q}]+bestaudio/best[height<={q}]"
        )
        opts["merge_output_format"] = "mp4"

    return opts

def find_output_file(downloaded, tmpdir):
    """Retrouve le fichier final même si yt-dlp a changé l'extension après merge."""
    if downloaded:
        candidate = downloaded[0]
        if os.path.exists(candidate):
            return candidate
        base = os.path.splitext(candidate)[0]
        for ext in [".mp4", ".mp3", ".m4a", ".webm", ".mkv"]:
            if os.path.exists(base + ext):
                return base + ext

    # Fallback : premier fichier non partiel dans tmpdir
    files = [f for f in glob.glob(os.path.join(tmpdir, "*"))
             if not f.endswith(".part") and os.path.isfile(f)]
    return files[0] if files else None

# ─── UI ────────────────────────────────────────────────────────────────────────
url = st.text_input("🔗 Lien de la vidéo", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns(2)
with col1:
    fmt = st.selectbox("🎬 Format", ["MP4 (vidéo)", "MP3 (audio)", "M4A (audio HQ)", "WebM (vidéo)"])
with col2:
    quality_map = {
        "Meilleure disponible": "best",
        "1080p": "1080",
        "720p":  "720",
        "480p":  "480",
        "360p":  "360",
    }
    quality_label = st.selectbox("📐 Qualité", list(quality_map.keys()), index=1)
    quality = quality_map[quality_label]

# ─── Aperçu ────────────────────────────────────────────────────────────────────
if url and st.button("🔍 Aperçu"):
    with st.spinner("Récupération des infos..."):
        try:
            with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True}) as ydl:
                info = ydl.extract_info(url, download=False)
            if info.get("thumbnail"):
                st.image(info["thumbnail"], width="stretch")
            st.markdown(f"""
            <div class="info-box">
                <div class="title-text">{info.get('title', '')}</div>
                <div class="meta-text">
                    {info.get('uploader', '')}
                    {' · ' + fmt_duration(info.get('duration')) if info.get('duration') else ''}
                    {' · ' + fmt_views(info.get('view_count')) if info.get('view_count') else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Impossible de récupérer les infos : {e}")

st.divider()

# ─── Téléchargement ────────────────────────────────────────────────────────────
if st.button("⬇️ Préparer le téléchargement", type="primary", width="stretch"):
    if not url.strip():
        st.warning("Colle un lien vidéo d'abord.")
    else:
        tmpdir     = tempfile.mkdtemp(prefix="vidfetch_")
        opts       = build_ydl_opts(fmt, quality, tmpdir)
        downloaded = []

        progress_bar = st.progress(0, text="Démarrage...")
        status_area  = st.empty()

        def progress_hook(d):
            if d["status"] == "downloading":
                try:
                    pct   = float(clean_ansi(d.get("_percent_str", "0%")).replace("%", ""))
                    speed = clean_ansi(d.get("_speed_str", ""))
                    eta   = clean_ansi(d.get("_eta_str", ""))
                    progress_bar.progress(
                        min(int(pct), 100),
                        text=f"Téléchargement… {pct:.0f}%  —  {speed}  —  ETA {eta}",
                    )
                except ValueError:
                    pass
            elif d["status"] == "finished":
                progress_bar.progress(100, text="Finalisation…")
                if d.get("filename"):
                    downloaded.append(d["filename"])

        opts["progress_hooks"] = [progress_hook]

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])

            filepath = find_output_file(downloaded, tmpdir)

            if not filepath:
                st.error("Fichier introuvable après téléchargement.")
                cleanup_tempdir(tmpdir)
            else:
                size_mb  = os.path.getsize(filepath) / (1024 * 1024)
                filename = os.path.basename(filepath)
                mime     = get_mime(filepath)

                progress_bar.empty()

                if size_mb > MAX_SIZE_MB:
                    st.warning(f"⚠️ Fichier volumineux ({size_mb:.0f} MB). L'envoi peut être lent.")

                status_area.success(f"✅ Prêt ! **{filename}** — {size_mb:.1f} MB")

                # ── Lecture en BytesIO puis nettoyage immédiat du disque ──────
                with open(filepath, "rb") as f:
                    file_bytes = io.BytesIO(f.read())

                cleanup_tempdir(tmpdir)  # suppression dès que les bytes sont en mémoire

                st.download_button(
                    label="💾 Télécharger sur mon appareil",
                    data=file_bytes,
                    file_name=filename,
                    mime=mime,
                    width="stretch",
                )
                st.caption(
                    "Le fichier ira dans ton dossier **Téléchargements**. "
                    "Le serveur a déjà supprimé sa copie."
                )

        except yt_dlp.utils.DownloadError as e:
            progress_bar.empty()
            cleanup_tempdir(tmpdir)
            err = str(e)
            if "429" in err or "blocked" in err.lower():
                st.error("🚫 Serveur bloqué par le site. Réessaie dans quelques minutes.")
            elif "Private" in err:
                st.error("🔒 Cette vidéo est privée.")
            else:
                st.error(f"Erreur de téléchargement : {err}")
        except Exception as e:
            progress_bar.empty()
            cleanup_tempdir(tmpdir)
            st.error(f"Erreur inattendue : {e}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Utilise [yt-dlp](https://github.com/yt-dlp/yt-dlp) · Usage personnel · Le serveur ne conserve aucun fichier.")