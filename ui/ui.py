from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)
from PySide6.QtGui import QCloseEvent
from .add_problem import AddProblemWindow
from .add_deck import AddDeckPopup


# CONSTANTS
from utils.program_paths import ProgramPaths
from utils.constants import PROGRAM_NAME

USER_DIR = ProgramPaths.get_user_dir()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.add_new_window: AddProblemWindow | None = None

        self.setWindowTitle(f"{PROGRAM_NAME}")

        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)

        # add deck button
        self.add_new_deck_button = QPushButton("Add new deck")
        self.add_new_deck_button.clicked.connect(self.show_add_deck_dialog)

        # add exercise button
        self.add_new_problem_button = QPushButton("Add new problem")
        self.add_new_problem_button.clicked.connect(
            self.show_add_problem_window
        )

        # adding element to container
        self.container_layout.addWidget(self.add_new_deck_button)
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
                QMessageBox.Yes | QMessageBox.No,  # type: ignore
                QMessageBox.No,  # type: ignore
            )

            if reply == QMessageBox.Yes:  # type: ignore
                QApplication.instance().closeAllWindows()  # type: ignore
                event.accept()
            else:
                event.ignore()

        else:
            QApplication.instance().closeAllWindows()  # type: ignore
            event.accept()

    def show_add_problem_window(self):
        # avoid destroying the window if it already exists
        if self.add_new_window is None:
            self.add_new_window = AddProblemWindow()
        self.add_new_window.show()

    def show_add_deck_dialog(self):
        self.add_new_deck_popup = AddDeckPopup()
        self.add_new_deck_popup.show()
        pass


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
