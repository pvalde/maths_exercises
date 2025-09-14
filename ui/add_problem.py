from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPlainTextEdit
from PySide6.QtGui import QFont, QFontMetrics
from PySide6.QtWebEngineWidgets import QWebEngineView
from ui.ui_utils import NoInternetProfile

# CONSTANTS
from utils.constants import PROGRAM_NAME
from utils.constants import MAIN_DIR 
from utils.constants import USER_MEDIA_QURL 
from utils.constants import MATHJAX3_PATH 

class AddProblemWindow(QWidget):
    """
    Window for adding new 'exercises' to the database.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add New")
        layout = QVBoxLayout()

        # Front Text ------------------------------------
        self.front_label = QLabel("Problem")
        self.front_edit = QPlainTextEdit(self)
        self.front_edit.setFont(QFont("Courier New", 11))
        # define tab width
        # TODO: change tabs with spaces
        self.front_edit.setTabStopDistance(
            QFontMetrics(self.front_edit.font()).horizontalAdvance(" ") * 2
        )

        # Back Text ------------------------------------
        self.back_label = QLabel("Solution")
        self.back_edit = QPlainTextEdit(self)
        self.back_edit.setFont(QFont("Courier New", 11))
        # define tab width
        # TODO: change tabs with spaces
        self.front_edit.setTabStopDistance(
            QFontMetrics(self.front_edit.font()).horizontalAdvance(" ") * 2
        )

        # html preview ---------------------------------
        self.html_label = QLabel("Preview")
        self.profile = NoInternetProfile()
        self.html_viewer = QWebEngineView(self.profile)

        self.html_viewer.setHtml("<br>")
        # self.html_viewer.load(QUrl("https://www.google.com"))
        self.front_edit.textChanged.connect(self.update_preview)
        self.back_edit.textChanged.connect(self.update_preview)

        # setting layout
        layout.addWidget(self.front_label)
        layout.addWidget(self.front_edit)
        layout.addWidget(self.back_label)
        layout.addWidget(self.back_edit)
        layout.addWidget(self.html_label)
        layout.addWidget(self.html_viewer)

        self.setLayout(layout)

    def update_preview(self) -> None:
        """
        Updates html preview with contents of self.front_edit and self.back_edit
        """
        self.html_viewer.setHtml("<br>")
        html_header: str = (
            """<head>
        <script>
        MathJax = {
          tex: {
            inlineMath: {'[+]': [['$', '$']]}
          },
          svg: {
            fontCache: 'global'
          }
        };
        </script>
        """
            + f'<script src="file://{MAIN_DIR}/{MATHJAX3_PATH}"></script>'
            + "</head>"
        )

        html_content: str = (
            f"<!DOCTYPE html>\n<html>\n{html_header}\n"
            f"<body>\n{self.front_edit.toPlainText()}\n"
            + f"<hr>\n"
            + f"{self.back_edit.toPlainText()}\n</body>\n</html>"
        )

        # print(html_content)

        self.html_viewer.setHtml(html_content, baseUrl=USER_MEDIA_QURL)
        self.html_viewer.update()
