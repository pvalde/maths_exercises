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
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QCloseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import (
    QWebEngineProfile,
    QWebEngineUrlRequestInterceptor,
    QWebEngineUrlRequestInfo,
)

PROGRAM_NAME: str = "Maths Exercises"


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


class AddExerciseWindow(QWidget):
    """
    Window for adding new 'exercises' to the database.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add New")
        layout = QVBoxLayout()

        # edit fields

        self.front_label = QLabel("Question")
        self.front_edit = QPlainTextEdit(self)

        self.back_label = QLabel("Answer")
        self.back_edit = QPlainTextEdit(self)

        # adding html preview

        self.html_label = QLabel("Preview")
        self.profile = NoInternetProfile()
        print("is profile off the record?", self.profile.isOffTheRecord())
        self.html_viewer = QWebEngineView(self.profile)

        self.html_viewer.setHtml("")
        # self.html_viewer.load(QUrl("https://www.google.com"))
        self.front_edit.textChanged.connect(self.on_text_changed)

        # setting layout
        layout.addWidget(self.front_label)
        layout.addWidget(self.front_edit)
        layout.addWidget(self.back_label)
        layout.addWidget(self.back_edit)
        layout.addWidget(self.html_label)
        layout.addWidget(self.html_viewer)

        self.setLayout(layout)

    def on_text_changed(self):
        self.html_viewer.setHtml("")
        self.html_viewer.setHtml(self.front_edit.toPlainText())
        self.html_viewer.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.add_new_window: AddExerciseWindow | None = None
        print(self.add_new_window)

        self.setWindowTitle(f"{PROGRAM_NAME}")

        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.label1 = QLabel("Label 1")
        self.label2 = QLabel("Label 2")

        self.container_layout.addWidget(self.label1)
        self.container_layout.addWidget(self.label2)

        # add exercise' window
        self.add_new_exercise_button = QPushButton("Add new exercise")
        self.add_new_exercise_button.clicked.connect(
            self.show_add_exercise_window
        )
        self.container_layout.addWidget(self.add_new_exercise_button)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        self.file_menu.addAction("Exit", self.close)

    def closeEvent(self, event: QCloseEvent):
        print("when closing, add_new_window is", self.add_new_window)
        if self.add_new_window is not None:
            reply = QMessageBox.question(
                self,
                "?",
                "?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if reply == QMessageBox.Yes:
                QApplication.instance().closeAllWindows()
                event.accept()
            else:
                event.ignore()

    def show_add_exercise_window(self):
        # avoid destroying the window if it already exists
        print(self.add_new_exercise_button)
        if self.add_new_window is None:
            self.add_new_window = AddExerciseWindow()
        self.add_new_window.show()


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
