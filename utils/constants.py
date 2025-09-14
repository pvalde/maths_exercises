from PySide6.QtCore import QUrl
from .program_paths import ProgramPaths
from pathlib import Path

# General
PROGRAM_NAME = "Maths Problems"
MAIN_DIR = Path(__file__).resolve().parent.parent

# Mathjax paths
MATHJAX4_PATH = "lib/mathjax4/tex-mml-chtml.js"
MATHJAX3_PATH = "lib/mathjax3/es5/tex-mml-chtml.js"

# QtWebEngineView
USER_MEDIA_QURL: QUrl = QUrl.fromLocalFile(ProgramPaths.get_user_media_dir())