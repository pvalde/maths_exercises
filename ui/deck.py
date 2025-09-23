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
)
from utils.constants import PROGRAM_NAME
from db.deck_db import DeckDB
from typing import Callable, List
from .ui_utils import decks_mem


class AddDeckPopup(QWidget):
    def __init__(self, show_function: Callable[[], None]):
        super().__init__()
        self.show_function = show_function
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
                f"Please provide a name for the deck.",
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

            self.show_function()
            decks_mem.update()

        else:

            self.deck_name_error = QMessageBox.critical(
                self,
                "Error",
                f"A deck with name '{deck_final_name}' already exists.",
            )


class DeckListWidget(QListWidget):
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
        Deletes the current deck from the DB.
        """

        # TODO
        print("deleting deck: ", deck_to_delete.text())

    def show_decks(self) -> None:
        """
        Shows the current decks in DB on the GUI.
        """
        # TODO: rewrite having in mine the delete of decks

        # get a list of current decks in DB
        decks_list = DeckDB.get_decks_all()

        # check if any deck in the DB is already in program's memory
        # -- first gather decks in a list
        self.items_list: List[QListWidgetItem] = []
        for item_i in range(self.count()):
            self.items_list.append(self.item(item_i))

        # -- check if any new deck is in the DB. If exists, keep it in the
        #    decks list (will be added later)
        for deck in self.items_list:
            if deck.text() in decks_list:
                decks_list.remove(deck.text())

        # -- add new decks to the list of QListWidgetItems
        for deck_name in decks_list:
            new_item = QListWidgetItem(deck_name)
            self.items_list.append(new_item)
            self.addItem(new_item)

        self.sortItems()
        # print(self.items_list)
