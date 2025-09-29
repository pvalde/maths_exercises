from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
    QListWidgetItem,
)
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, Signal
from typing import List, Dict, override

from ui.add_problem import AddProblemWindow
from ui.deck import AddDeckPopup, DeckListWidget

# CONSTANTS
from ui.ui_utils import DeckUpdEmitter
from utils.program_paths import ProgramPaths
from utils.constants import PROGRAM_NAME

USER_DIR = ProgramPaths.get_user_dir()


class MainWindow(QMainWindow, DeckUpdEmitter):
    decks_updated = Signal()

    def __init__(self):
        super().__init__()

        self.child_window: Dict[
            str, AddProblemWindow | AddDeckPopup | None
        ] = {}

        self.setWindowTitle(f"{PROGRAM_NAME}")

        self.container = QWidget()
        self.setCentralWidget(self.container)

        # containers
        self.main_container = QVBoxLayout(self.container)
        self.add_buttons_container = QHBoxLayout()

        # decks_container
        self.decks_container_label = QLabel("<h1>Decks</h1>")
        self.decks_container_label.setTextFormat(Qt.RichText)  # type: ignore

        self.deck_list_widget = DeckListWidget()
        self.decks_items: List[QListWidgetItem] = []
        self.show_decks()

        # add deck button
        self.add_new_deck_button = QPushButton("Add new deck")
        self.add_new_deck_button.clicked.connect(self.show_add_deck_dialog)

        # add exercise button
        self.add_new_problem_button = QPushButton("Add new problem")
        self.add_new_problem_button.clicked.connect(
            self.show_add_problem_window
        )

        # adding element to containers

        self.add_buttons_container.addWidget(self.add_new_deck_button)
        self.add_buttons_container.addWidget(self.add_new_problem_button)
        self.main_container.addLayout(self.add_buttons_container)
        self.main_container.addWidget(self.decks_container_label, alignment=Qt.AlignCenter)  # type: ignore
        self.main_container.addWidget(self.deck_list_widget)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        # Exit QAction
        self.file_menu.addAction("Exit", self.close)

    def closeEvent(self, event: QCloseEvent):
        # debugging
        for key, value in self.child_window.items():
            print(f"'{key}': {value}")

        if any(value is not None for value in self.child_window.values()):
            reply = QMessageBox.question(
                self,
                "Warning",
                "There are active windows opened."
                + "Would you like to quit and discard any work anyways?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                QApplication.quit()
            else:
                event.ignore()

        else:
            QApplication.quit()

    def show_add_problem_window(self):
        # avoid destroying the window if it already exists
        window = self.child_window.get("add_problem", None)
        if window is None:
            self.child_window["add_problem"] = AddProblemWindow()
            self.child_window["add_problem"].closed.connect(
                lambda: self.set_child_window_to_none("add_problem")
            )

        # to avoid pyright error
        if self.child_window["add_problem"] is not None:
            self.child_window["add_problem"].show()

    def show_add_deck_dialog(self) -> None:
        window = self.child_window.get("deck_dialog", None)
        if window is None:
            self.child_window["deck_dialog"] = AddDeckPopup()
            self.child_window["deck_dialog"].closed.connect(
                lambda: self.set_child_window_to_none("deck_dialog")
            )

            self.child_window["deck_dialog"].decks_updated.connect(
                self.decks_updated_emitter
            )

        # to avoid pyright error
        if self.child_window["deck_dialog"] is not None:
            self.child_window["deck_dialog"].show()

    def set_child_window_to_none(self, window_name: str) -> None:
        self.child_window[f"{window_name}"] = None

    def show_decks(self):
        self.deck_list_widget.update_list_of_decks()

    @override
    def decks_updated_emitter(self) -> None:

        problem_window: AddProblemWindow | AddDeckPopup | None = (
            self.child_window.get("add_problem", None)
        )
        if (problem_window is not None) and (
            type(problem_window) is AddProblemWindow
        ):
            AddProblemWindow.decks_updated_reciever(problem_window)

        self.deck_list_widget.decks_updated_reciever()


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
