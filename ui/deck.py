from typing import override
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QListWidget,
    QListWidgetItem,
    QMenu,
)

from PySide6.QtGui import (
    QContextMenuEvent,
    QShortcut,
    QKeySequence,
    QAction,
    QCloseEvent,
)
from utils.constants import PROGRAM_NAME
from db.deck_db import DeckDB
from ui.ui_utils import DeckUpdEmitter, DeckUpdReciever


class AddDeckPopup(QWidget, DeckUpdEmitter):
    """
    QWidget that works as a popup that prompts the user to add a new deck.
    """

    closed = Signal(bool)
    decks_updated = Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add Deck")

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.name_layout = QHBoxLayout()

        self.deck_name_label = QLabel("Name")
        self.deck_name = QLineEdit()
        self.name_layout.addWidget(self.deck_name_label)
        self.name_layout.addWidget(self.deck_name)

        self.main_layout.addLayout(self.name_layout)

        self.add_deck_button = QPushButton("Add Deck")
        self.main_layout.addWidget(self.add_deck_button)
        self.add_deck_button.clicked.connect(self.add_deck)

        # add shortcut (Return)
        self.add_deck_shortcut = QShortcut(QKeySequence("Return"), self)
        self.add_deck_shortcut.activated.connect(self.add_deck)

    def add_deck(self) -> None:
        deck_final_name = self.deck_name.text().strip()

        if deck_final_name.strip() == "":
            self.deck_name_error = QMessageBox.critical(
                self,
                "Error",
                "Please provide a name for the deck.",
            )

        elif not DeckDB.deck_exists(deck_final_name):

            try:
                DeckDB.add_deck(deck_final_name)
            except Exception as e:
                self.add_deck_error = QMessageBox.critical(
                    self,
                    "Error",
                    f"There was a problem adding the deck '{deck_final_name}': {e}.".strip(
                        "."
                    ),
                )
                return

            else:
                self.add_deck_success = QMessageBox.information(
                    self,
                    "Success",
                    f"The deck '{deck_final_name}' has been added to the DB.",
                )

            self.decks_updated_emitter()
            self.closed.emit(True)
            self.close()

        else:
            self.deck_name_error = QMessageBox.critical(
                self,
                "Error",
                f"A deck with name '{deck_final_name}' already exists.",
            )

    def closeEvent(self, event: QCloseEvent, /) -> None:
        self.closed.emit(True)
        return super().closeEvent(event)

    @override
    def decks_updated_emitter(self) -> None:
        self.decks_updated.emit(True)


class DeckListWidget(QListWidget, DeckUpdEmitter, DeckUpdReciever):
    decks_updated = Signal(bool)

    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        """
        Defines a custom rigthclick contextMenuEvent for the list of decks. It
        only activates when a deck in the list is clicked.
        """
        item = self.itemAt(event.pos())  # get the item

        if item is not None:  # type: ignore
            context_menu = QMenu()
            delete_action = QAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_deck(item))

            context_menu.addAction(delete_action)

            context_menu.exec(event.globalPos())

    def delete_deck(self, deck_to_delete: QListWidgetItem) -> None:
        """
        Deletes the current deck from the self consulting the DB.
        """
        try:
            DeckDB.remove_deck(deck_to_delete.text())
        except Exception as e:
            QMessageBox.critical(self, "Error", f"{e}")
            return
        print("deleting deck: ", deck_to_delete.text())
        self._update_list_of_decks()
        self.decks_updated_emitter()

    def _update_list_of_decks(self) -> None:
        """
        Updates the current list of decks according to DB.
        """

        print("DeckListWidget retrieving list of decks from DB")

        # remove all items from the current list
        n_of_decks_in_mem = self.count()
        for i in range(n_of_decks_in_mem):
            self.takeItem(n_of_decks_in_mem - 1 - i)

        # get a list of current decks in DB
        decks_in_db = sorted(DeckDB.get_decks_all())

        # add decks to self
        self.addItems(decks_in_db)

    @override
    def decks_updated_reciever(self) -> None:
        self._update_list_of_decks()

    @override
    def decks_updated_emitter(self) -> None:
        self.decks_updated.emit(True)
