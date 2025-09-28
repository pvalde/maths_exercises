from PySide6.QtWidgets import (
    QPushButton,
    QWidget,
    QLabel,
    QVBoxLayout,
    QPlainTextEdit,
    QComboBox,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics, QMouseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from ui.ui_utils import (
    NoInternetProfile,
    update_decks_from_db,
)
from db.deck_db import DeckDB
from db.problem_db import ProblemDB

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
        """ """
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add New")
        layout = QVBoxLayout()

        # Deck selection --------------------------------
        self.deckSelectorTitle = QLabel("Deck")
        self.deckSelector = DeckSelector()

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

        # add deck button
        self.button = QPushButton("Add Problem")
        self.button.clicked.connect(self.add_problem)

        # setting layout

        # -- deck selector ----------------
        layout.addWidget(self.deckSelectorTitle)
        layout.addWidget(self.deckSelector)

        # -- front ------------------------
        layout.addWidget(self.front_label)
        layout.addWidget(self.front_edit)

        # -- back -------------------------
        layout.addWidget(self.back_label)
        layout.addWidget(self.back_edit)

        # -- preview ----------------------
        layout.addWidget(self.html_label)
        layout.addWidget(self.html_viewer)

        layout.addWidget(self.button)

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
            + "<hr>\n"
            + f"{self.back_edit.toPlainText()}\n</body>\n</html>"
        )

        # print(html_content)

        self.html_viewer.setHtml(html_content, baseUrl=USER_MEDIA_QURL)
        self.html_viewer.update()

    def add_problem(self) -> None:
        content = {
            "question": self.front_edit.toPlainText(),
            "answer": self.back_edit.toPlainText(),
        }

        ProblemDB.add_deck(
            content=content, deck=self.deckSelector.currentText()
        )
        print(f"new problem added to '{self.deckSelector.currentText()}'!!!")
        self.close()


class DeckSelector(QComboBox):
    def __init__(self):
        super().__init__()

        # deck key-value pair in ui.ui_utils.update_decks_from_db
        if "DeckSelector" not in update_decks_from_db:
            update_decks_from_db["DeckSelector"] = True

        self.update_list_of_decks()

    def update_list_of_decks(self):
        """
        Checks if the decks table in the db has been modified. If true, update
        the DeckSelector's list of decks according to that.
        """
        if update_decks_from_db["DeckSelector"]:
            # delete the current list in DeckSelector class
            n_of_items = self.count()
            for i in range(n_of_items):
                self.removeItem(n_of_items - 1 - i)

            print("DeckSelector retrieving list of decks from DB.")
            self.addItems(sorted(DeckDB.get_decks_all()))
            update_decks_from_db["DeckSelector"] = False

    def mousePressEvent(self, event: QMouseEvent):
        """
        Overrides default implementation to detect clicks. It runs
        self.add_decks()
        """
        if event.button() == Qt.LeftButton:  # type: ignore
            self.update_list_of_decks()

        super().mousePressEvent(event)  # calls the default behavior
