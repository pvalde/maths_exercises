from PySide6.QtWidgets import (
    QApplication,
    QLayout,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QLabel,
)
from PySide6.QtGui import QCloseEvent
from PySide6.QtCore import Qt, Signal
from typing import List, Dict, override, Tuple

from ui.add_problem import AddProblemWindow
from ui.deck import AddDeckPopup, DeckListWidget

from ui.ui_utils import DeckUpdEmitter, DeckUpdReciever
from utils.program_paths import ProgramPaths
from utils.constants import PROGRAM_NAME

USER_DIR = ProgramPaths.get_user_dir()


class MainWindow(QMainWindow, DeckUpdEmitter):
    decks_updated = Signal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle(f"{PROGRAM_NAME}")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        self.child_window: Dict[
            str, AddProblemWindow | AddDeckPopup | None
        ] = {}

        self.decks_updated_recievers: List[DeckUpdReciever] = []

        # create main_container
        self.main_container = QWidget()
        self.setCentralWidget(self.main_container)
        self.main_container = QVBoxLayout(self.main_container)

        self.main_sub_containers: List[QLayout | QWidget] = []

        # adding containers to list of main_sub_containers
        self.main_sub_containers.append(self._create_buttons_container())
        for container in self._create_decks_container():
            self.main_sub_containers.append(container)
            self.main_sub_containers.append(container)

        # adding containers in main_sub_container to main_container object
        for container in self.main_sub_containers:
            if isinstance(container, QLayout):
                self.main_container.addLayout(container)
            elif isinstance(container, QWidget):
                self.main_container.addWidget(container)

        # Exit QAction
        self.file_menu.addAction("Exit", self.close)

    def _create_buttons_container(self) -> QHBoxLayout:
        add_buttons_container = QHBoxLayout()

        # add deck button
        add_new_deck_button = QPushButton("Add new deck")
        add_new_deck_button.clicked.connect(self._show_add_deck_dialog)

        # add exercise button
        add_new_problem_button = QPushButton("Add new problem")
        add_new_problem_button.clicked.connect(self._show_add_problem_window)

        add_buttons_container.addWidget(add_new_deck_button)
        add_buttons_container.addWidget(add_new_problem_button)

        return add_buttons_container

    def _create_decks_container(self) -> Tuple[QLabel, DeckListWidget]:
        decks_container_label = QLabel("<h1>Decks</h1>")
        decks_container_label.setTextFormat(Qt.RichText)  # pyright: ignore

        deck_list_widget = DeckListWidget()
        self.decks_updated_recievers.append(deck_list_widget)
        deck_list_widget.decks_updated_reciever()

        return (decks_container_label, deck_list_widget)

    def closeEvent(self, event: QCloseEvent):

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

    def _show_add_problem_window(self):
        # avoid destroying the window if it already exists
        window = self.child_window.get("add_problem", None)
        if window is None:
            self.child_window["add_problem"] = AddProblemWindow()
            self.child_window["add_problem"].closed.connect(
                lambda: self._set_child_window_to_none("add_problem")
            )

        # to avoid pyright error
        if self.child_window["add_problem"] is not None:
            self.child_window["add_problem"].show()

    def _show_add_deck_dialog(self) -> None:
        window = self.child_window.get("deck_dialog", None)
        if window is None:
            self.child_window["deck_dialog"] = AddDeckPopup()
            self.child_window["deck_dialog"].closed.connect(
                lambda: self._set_child_window_to_none("deck_dialog")
            )

            self.child_window["deck_dialog"].decks_updated.connect(
                self.decks_updated_emitter
            )

        # to avoid pyright error
        if self.child_window["deck_dialog"] is not None:
            self.child_window["deck_dialog"].show()

    def _set_child_window_to_none(self, window_name: str) -> None:
        self.child_window[f"{window_name}"] = None

    @override
    def decks_updated_emitter(self) -> None:
        for element in self.decks_updated_recievers:
            element.decks_updated_reciever()

        for element in self.child_window.values():
            if element is not None and isinstance(element, DeckUpdReciever):
                element.decks_updated_reciever()


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()
