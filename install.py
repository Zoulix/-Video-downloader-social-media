"""
install.py — Installation automatique de VidFetch
Installe : Python packages + ffmpeg (avec ajout au PATH)
Usage     : python install.py
"""

import os
import sys
import platform
import subprocess
import zipfile
import tarfile
import shutil
import urllib.request

SYSTEM = platform.system()  # 'Windows', 'Darwin', 'Linux'


# ─── Utilitaires ───────────────────────────────────────────────────────────────

def log(msg, emoji=""):
    print(f"{emoji}  {msg}" if emoji else msg)

def run(cmd, check=True):
    """Exécute une commande shell et affiche la sortie."""
    log(f"→ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    result = subprocess.run(cmd, shell=isinstance(cmd, str), check=check,
                            capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr.strip():
        print(result.stderr.strip())
    return result

def download_file(url, dest):
    log(f"Téléchargement de {os.path.basename(dest)}...")
    def progress(count, block_size, total_size):
        pct = int(count * block_size * 100 / total_size) if total_size > 0 else 0
        print(f"\r  {min(pct,100)}%", end="", flush=True)
    urllib.request.urlretrieve(url, dest, reporthook=progress)
    print()  # saut de ligne après la barre


# ─── 1. Packages Python ────────────────────────────────────────────────────────

def install_python_packages():
    log("Installation des packages Python...", "📦")
    packages = ["streamlit", "yt-dlp"]
    run([sys.executable, "-m", "pip", "install", "--upgrade"] + packages)
    log("Packages installés ✓", "✅")


# ─── 2. ffmpeg ─────────────────────────────────────────────────────────────────

FFMPEG_DIR = os.path.join(os.path.expanduser("~"), "ffmpeg")

def ffmpeg_already_installed():
    """Vérifie si ffmpeg est déjà accessible dans le PATH."""
    return shutil.which("ffmpeg") is not None

def install_ffmpeg_windows():
    url  = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    dest = os.path.join(os.path.expanduser("~"), "ffmpeg_download.zip")

    download_file(url, dest)
    log("Extraction...", "📂")

    with zipfile.ZipFile(dest, "r") as z:
        # Le zip contient un dossier racine du type ffmpeg-7.x-essentials_build/
        names   = z.namelist()
        root    = names[0].split("/")[0]
        z.extractall(os.path.expanduser("~"))

    extracted = os.path.join(os.path.expanduser("~"), root)
    bin_dir   = os.path.join(extracted, "bin")

    # Déplacer vers ~/ffmpeg/bin pour un chemin stable
    if os.path.exists(FFMPEG_DIR):
        shutil.rmtree(FFMPEG_DIR)
    shutil.move(extracted, FFMPEG_DIR)
    os.remove(dest)

    final_bin = os.path.join(FFMPEG_DIR, "bin")
    add_to_path_windows(final_bin)
    return final_bin

def add_to_path_windows(bin_dir):
    """Ajoute bin_dir au PATH utilisateur (permanent) via le registre Windows."""
    import winreg
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Environment",
        0,
        winreg.KEY_READ | winreg.KEY_WRITE,
    )
    try:
        current, _ = winreg.QueryValueEx(key, "PATH")
    except FileNotFoundError:
        current = ""

    if bin_dir.lower() not in current.lower():
        new_path = current + ";" + bin_dir if current else bin_dir
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        log(f"PATH mis à jour → {bin_dir}", "🔧")
    else:
        log("ffmpeg déjà dans le PATH Windows.", "ℹ️")

    winreg.CloseKey(key)
    log("⚠️  Ferme et rouvre ton terminal pour que le PATH soit pris en compte.")

def install_ffmpeg_mac():
    """Installe ffmpeg via Homebrew (le plus simple sur macOS)."""
    if shutil.which("brew") is None:
        log("Installation de Homebrew...", "🍺")
        brew_install = (
            '/bin/bash -c "$(curl -fsSL '
            'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        )
        run(brew_install)
    log("Installation de ffmpeg via Homebrew...", "🍺")
    run(["brew", "install", "ffmpeg"])

def install_ffmpeg_linux():
    """Installe ffmpeg via apt (Debian/Ubuntu)."""
    log("Installation de ffmpeg via apt...", "🐧")
    run(["sudo", "apt-get", "update", "-y"])
    run(["sudo", "apt-get", "install", "-y", "ffmpeg"])

def install_ffmpeg():
    log("Vérification de ffmpeg...", "🔍")
    if ffmpeg_already_installed():
        log(f"ffmpeg déjà installé : {shutil.which('ffmpeg')}", "✅")
        return

    log("ffmpeg non trouvé — installation en cours...", "⚙️")

    if SYSTEM == "Windows":
        bin_dir = install_ffmpeg_windows()
        # Pour la session Python courante, on ajoute aussi au PATH en mémoire
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

    elif SYSTEM == "Darwin":
        install_ffmpeg_mac()

    elif SYSTEM == "Linux":
        install_ffmpeg_linux()

    else:
        log(f"Système non reconnu : {SYSTEM}. Installe ffmpeg manuellement.", "⚠️")
        return

    # Vérification finale
    if shutil.which("ffmpeg"):
        ver = subprocess.check_output(["ffmpeg", "-version"], text=True).split("\n")[0]
        log(f"ffmpeg installé ✓ — {ver}", "✅")
    else:
        log("ffmpeg installé mais pas encore dans le PATH de ce terminal.", "⚠️")
        log("Ferme et rouvre le terminal, puis relance : ffmpeg -version")


# ─── 3. Vérification finale ────────────────────────────────────────────────────

def check_all():
    log("\n── Vérification finale ──────────────────────────────")
    ok = True
    for tool, cmd in [("streamlit", ["streamlit", "--version"]),
                      ("yt-dlp",    ["yt-dlp",    "--version"]),
                      ("ffmpeg",    ["ffmpeg",     "-version"])]:
        path = shutil.which(cmd[0])
        if path:
            version = subprocess.check_output(cmd, text=True,
                          stderr=subprocess.DEVNULL).split("\n")[0]
            log(f"{tool:12} ✓  {version}", "  ")
        else:
            log(f"{tool:12} ✗  non trouvé", "  ")
            ok = False

    print()
    if ok:
        log("Tout est installé ! Lance l'app avec :", "🚀")
        log("   streamlit run vidfetch_app.py")
    else:
        log("Certains outils manquent. Voir les messages ci-dessus.", "⚠️")


# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  VidFetch — Installation automatique")
    print(f"  Système détecté : {SYSTEM} ({platform.machine()})")
    print("=" * 55)
    print()

    install_python_packages()
    print()
    install_ffmpeg()
    print()
    check_all()
