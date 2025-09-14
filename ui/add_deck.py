from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)

from PySide6.QtGui import QShortcut, QKeySequence
from utils.constants import PROGRAM_NAME
from db.deck_db import DeckDB


class AddDeckPopup(QWidget):
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
                f"Please provide a name for the deck.",
            )

        elif not DeckDB.deck_exists(deck_final_name):

            try:
                DeckDB.add_deck(deck_final_name)
            except Exception as e:
                self.add_deck_error = QMessageBox.critical(
                    self,
                    "Error",
                    f"There was a problem adding the deck '{deck_final_name}': {e}.".strip("."),
                )
                return

            else:
                self.add_deck_success = QMessageBox.information(
                    self,
                    "Success",
                    f"The deck '{deck_final_name}' has been added to the DB.",
                )

        else:

            self.deck_name_error = QMessageBox.critical(
                self,
                "Error",
                f"A deck with name '{deck_final_name}' already exists.",
            )
