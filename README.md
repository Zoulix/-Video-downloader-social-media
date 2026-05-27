<<<<<<< HEAD
# 📹 Social Media Video Downloader

Un outil puissant et facile à utiliser pour télécharger des vidéos directement depuis vos plateformes de réseaux sociaux préférées.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

## 📚 Sommaire

- [1. À propos du projet](#1-à-propos-du-projet)
- [2. Réalisation](#2-réalisation)
- [3. Prérequis](#3-prérequis)
- [4. Installation](#4-installation)
- [5. Utilisation](#5-utilisation)
- [6. Structure du projet](#6-structure-du-projet)
- [7. Cas d'usage](#7-cas-dusage)
- [8. Configuration](#8-configuration)
- [9. Dépannage](#9-dépannage)
- [10. Contribution](#10-contribution)
- [11. Avertissement juridique](#11-avertissement-juridique)

## 1. À propos du projet

**Social Media Video Downloader** est une application Python qui vous permet de télécharger facilement des vidéos à partir de diverses plateformes de réseaux sociaux populaires. Que vous vouliez conserver vos vidéos préférées, créer une collection personnelle ou télécharger du contenu pour une utilisation hors ligne, cet outil vous offre une solution simple et efficace.

### 1.1. Fonctionnalités principales

-  **Support de multiples plateformes** : Téléchargez des vidéos depuis YouTube, Instagram, TikTok, Facebook, Twitter, et bien d'autres
-  **Téléchargement rapide** : Extraction et téléchargement optimisés pour une performance maximale
-  **Qualité customizable** : Choisissez la résolution et le format de vidéo selon vos préférences
-  **Gestion intelligente des fichiers** : Organisation automatique des vidéos téléchargées
-  **Support des playlists** : Téléchargez plusieurs vidéos en une seule opération
-  **Sécurisé et stable** : Code robuste avec gestion complète des erreurs
-  **Interface intuitive** : Interface utilisateur simple et accessible à tous
-  **Extensible** : Architecture modulaire pour ajouter facilement de nouvelles plateformes


## 2. Réalisation

Cette application a été développée en **Python** avec une architecture modulaire et évolutive.

- Le cœur du projet utilise **`yt-dlp`** pour l'extraction et le téléchargement des flux vidéo/audio.
- Le code est organisé en modules :
  - **`src/downloader.py`** pour la logique principale de téléchargement
  - **`src/platforms/`** pour les gestionnaires spécifiques à chaque réseau social
  - **`src/utils/`** pour la validation d'URL, la configuration et le logging
  - **`src/gui/`** pour une interface graphique optionnelle
- Chaque plateforme est traitée par un module dédié, ce qui rend l'ajout d'un nouveau réseau social simple et rapide.
- La configuration est centralisée dans **`config/config.json`** pour définir le dossier de sortie, la qualité, le timeout et le nombre de tentatives.
- Le flux de traitement est :
  1. Validation de l'URL
  2. Détection de la plateforme
  3. Extraction des informations de la vidéo
  4. Téléchargement et conversion
  5. Sauvegarde et journalisation
- Des tests unitaires permettent de vérifier le comportement des modules clés et de garder le projet stable.
---

## 3. Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

- **Python 3.7+** : [Télécharger Python](https://www.python.org/downloads/)
- **pip** : Gestionnaire de paquets Python (inclus avec Python)
- **git** : Pour cloner le repository (optionnel)

### 3.1.Vérifier votre installation

```bash
python --version
pip --version
```

---

## 4. Installation

### 4.1. Cloner le repository

```bash
git clone https://github.com/username/Video-downloader-social-media.git
cd Video-downloader-social-media
```

Ou téléchargez le ZIP depuis GitHub et extrayez-le.

### 4.2. Créer un environnement virtuel

Il est recommandé d'utiliser un environnement virtuel Python pour isoler les dépendances du projet.

**Sous Windows :**
```bash
python -m venv env
env\Scripts\activate
```

**Sous macOS/Linux :**
```bash
python3 -m venv env
source env/bin/activate
```

### 4.3. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les dépendances principales incluent :
- `yt-dlp` : Pour l'extraction vidéo haute performance
- `requests` : Pour les requêtes HTTP
- `beautifulsoup4` : Pour le parsing HTML
- Et d'autres librairies essentielles

---

## 5. Utilisation

### 5.1. Mode ligne de commande

```bash
python downloader.py "URL_DE_LA_VIDEO"
```

**Exemples :**

```bash
# Télécharger depuis YouTube
python downloader.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Télécharger depuis Instagram
python downloader.py "https://www.instagram.com/p/ABC123/"

# Télécharger depuis TikTok
python downloader.py "https://www.tiktok.com/@user/video/123456789"
```

### 5.2. Options disponibles

```bash
# Télécharger en haute qualité (1080p)
python downloader.py "URL" --quality 1080

# Télécharger au format MP3 (audio uniquement)
python downloader.py "URL" --audio-only

# Spécifier le dossier de destination
python downloader.py "URL" --output "./mes_videos"

# Afficher les informations sans télécharger
python downloader.py "URL" --info-only
```

### 5.3. Mode interface graphique (si disponible)

```bash
python gui.py
```

---

## 6. Structure du projet

```
Video-downloader-social-media/
│
├── README.md                 # Ce fichier
├── requirements.txt          # Dépendances Python
├── setup.py                  # Configuration du projet
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Point d'entrée principal
│   ├── downloader.py        # Logique de téléchargement
│   │
│   ├── platforms/           # Support de chaque plateforme
│   │   ├── youtube.py
│   │   ├── instagram.py
│   │   ├── tiktok.py
│   │   └── ...
│   │
│   ├── utils/               # Utilitaires et helpers
│   │   ├── validator.py     # Validation des URLs
│   │   ├── config.py        # Configuration
│   │   └── logger.py        # Logging
│   │
│   └── gui/                 # Interface graphique (optionnel)
│       └── interface.py
│
├── tests/                    # Tests unitaires
│   ├── test_downloader.py
│   └── test_platforms.py
│
├── config/                   # Fichiers de configuration
│   └── config.json
│
└── env/                      # Environnement virtuel Python
```

---

## 7. Cas d'usage

- ✅ **Créer une collection personnelle** : Téléchargez et organisez vos vidéos préférées
- ✅ **Accès hors ligne** : Regardez vos vidéos sans connexion internet
- ✅ **Archivage** : Préservez le contenu avant suppression
- ✅ **Création de contenu** : Téléchargez des ressources pour l'édition vidéo
- ✅ **Recherche et analyse** : Collectez des données vidéo à des fins académiques

---

## 8. Configuration

Les paramètres peuvent être configurés dans `config/config.json` :

```json
{
  "output_directory": "./videos",
  "default_quality": "best",
  "audio_only": false,
  "max_concurrent_downloads": 3,
  "timeout": 60,
  "retries": 3
}
```

---

## 9. Dépannage

### 9.1. Problème : "Module not found"
**Solution :** Assurez-vous que l'environnement virtuel est activé
```bash
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate
```

### 9.2. Problème : "URL non valide"
**Solution :** Vérifiez que l'URL est complète et correcte. Essayez avec une URL simple d'abord.

### 9.3. Problème : Téléchargement lent
**Solution :** 
- Réduisez la qualité avec `--quality 480`
- Vérifiez votre connexion internet
- Augmentez le timeout : `--timeout 120`

### 9.4. Problème : La plateforme n'est pas supportée
**Solution :** Consultez la liste des plateformes supportées ou créez une issue GitHub pour demander le support.

---

## 10. Contribution

Les contributions sont les bienvenues ! Voici comment vous pouvez aider :

### 10.1. Signaler un bug
1. Allez sur [Issues](https://github.com/username/Video-downloader-social-media/issues)
2. Cliquez sur "New Issue"
3. Décrivez le problème avec des détails et des étapes pour le reproduire

### 10.2. Proposer une amélioration
1. Forkez le repository
2. Créez une branche pour votre feature (`git checkout -b feature/amazing-feature`)
3. Committez vos changements (`git commit -m 'Add amazing feature'`)
4. Pushez vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrez une Pull Request

### 10.3. Directives de contribution
- Respectez le style de code existant
- Écrivez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Assurez-vous que tous les tests passent

---

## 11. Avertissement juridique

**Avant d'utiliser cet outil, veuillez noter :**

- Respectez les **conditions d'utilisation** des plateformes de réseaux sociaux
- Obtenez la **permission des propriétaires de contenu** avant de télécharger
- N'utilisez pas cet outil pour les activités **illégales ou contraires à l'éthique**
- Certaines juridictions peuvent avoir des **restrictions légales** sur le téléchargement de contenu
- L'auteur n'est **pas responsable** de l'utilisation abusive du logiciel

Utilisez toujours cet outil **de manière responsable et légale**.

---

##  Support et contact

- **Questions** : Ouvrez une [Discussion](https://github.com/Zoulix/Video-downloader-social-media/discussions)
- **Bugs** : Signalez sur [Issues](https://github.com/Zoulix/Video-downloader-social-media/issues)

---

##  Remerciements

Merci à :
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) pour l'extraction vidéo
- Tous les contributeurs et utilisateurs
- La communauté open-source

---

##  Feuille de route

- [x] Support YouTube
- [ ] Support Instagram
- [ ] Support TikTok
- [ ] Interface graphique
- [ ] Téléchargement par batch
- [ ] Configuration avancée
- [ ] Support mobile
- [ ] Extension navigateur
---

**Made with ❤️ by [Zoul](https://github.com/Zoulix) and [Christ](https://github.com/christ1379)**

Dernière mise à jour : May 2026
=======
# VidDownloader
Create an application to download videos from social media directly on your device.
>>>>>>> 40de896a27de4aaafd5d61ad3b2003f0d8efaceb
