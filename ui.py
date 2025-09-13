from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QMessageBox,
)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QCloseEvent, QFont, QFontMetrics
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInterceptor,
    QWebEngineUrlRequestInfo,
)
from pathlib import Path

import platformFuns

USER_DIR = platformFuns.get_user_dir()
# the trailing forward slash is essential. Without it the QtWebEngineView
# will interpret the base url as a file (?)
USER_MEDIA_DIR = QUrl.fromLocalFile(platformFuns.get_user_media_dir())
SRC_DIR = Path(__file__).resolve().parent
PROGRAM_NAME: str = "Maths Problems"
MATHJAX4_PATH = "lib/mathjax4/tex-mml-chtml.js"
MATHJAX3_PATH = "lib/mathjax3/es5/tex-mml-chtml.js"


class NoInternetProfile(QWebEngineProfile):
    """
    Custom QWebEngineProfile object that returns one with the default profile
    (off-the-record) and with internet access blocked.
    """

    def __init__(self):
        super().__init__()

        self.defaultProfile()
        self.interceptor = self.BlockedRequestInterceptor()
        self.setUrlRequestInterceptor(self.interceptor)

    class BlockedRequestInterceptor(QWebEngineUrlRequestInterceptor):
        """
        Custom class of QWebEngineUrlRequestInterceptor that sets a
        QWebEngineProfile to block any access to internet.
        """

        def interceptRequest(self, info: QWebEngineUrlRequestInfo):
            url = info.requestUrl()
            if url.scheme() in ["file", "data"]:
                # Allow local files and local data
                info.block(False)
            else:
                # Block all requests
                info.block(True)


class AddProblemWindow(QWidget):
    """
    Window for adding new 'exercises' to the database.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add New")
        layout = QVBoxLayout()

        # print(
        #     f"MATHJAX4_PATH: {MATHJAX4_PATH}\n",
        #     f"MATHJAX3_PATH: {MATHJAX3_PATH}\n",
        #     f"BASE_URL: {USER_MEDIA_DIR}\n",
        #     f"SRC_DIR: {SRC_DIR}\n",
        # )

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
            + f'<script src="file://{SRC_DIR}/{MATHJAX3_PATH}"></script>'
            + "</head>"
        )

        html_content: str = (
            f"<!DOCTYPE html>\n<html>\n{html_header}\n"
            f"<body>\n{self.front_edit.toPlainText()}\n"
            + f"<hr>\n"
            + f"{self.back_edit.toPlainText()}\n</body>\n</html>"
        )

        # print(html_content)

        self.html_viewer.setHtml(html_content, baseUrl=USER_MEDIA_DIR)
        self.html_viewer.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.add_new_window: AddProblemWindow | None = None

        self.setWindowTitle(f"{PROGRAM_NAME}")

        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)

        # add exercise' window
        self.add_new_problem_button = QPushButton("Add new problem")
        self.add_new_problem_button.clicked.connect(
            self.show_add_problem_window
        )
        self.container_layout.addWidget(self.add_new_problem_button)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        self.file_menu.addAction("Exit", self.close)

    def closeEvent(self, event: QCloseEvent):
        if self.add_new_window is not None:
            reply = QMessageBox.question(
                self,
                "Warning",
                "There is an exercise card that has not been saved yet. "
                + "Would you like to quit anyways?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                QApplication.instance().closeAllWindows()
                event.accept()
            else:
                event.ignore()

    def show_add_problem_window(self):
        # avoid destroying the window if it already exists
        if self.add_new_window is None:
            self.add_new_window = AddProblemWindow()
        self.add_new_window.show()


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
