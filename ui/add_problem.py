from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPlainTextEdit,
    QComboBox,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontMetrics, QMouseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from typing import List
from ui.ui_utils import NoInternetProfile

# CONSTANTS
from utils.constants import PROGRAM_NAME
from utils.constants import MAIN_DIR
from utils.constants import USER_MEDIA_QURL
from utils.constants import MATHJAX3_PATH
from .ui_utils import decks_mem


class AddProblemWindow(QWidget):
    """
    Window for adding new 'exercises' to the database.
    """

    def __init__(self):
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


class DeckSelector(QComboBox):
    def __init__(self):
        super().__init__()
        self.list_of_decks: List[str] = []
        self.update_list_of_decks()

    def update_list_of_decks(self):
        """
        Checks the current list of decks in memory and updates the DeckSelector 
        list of decks according to that.
        """

        # delete the current list
        n_of_items = self.count()
        for i in range (n_of_items):
            self.removeItem(n_of_items-1 - i)

        self.addItems(decks_mem.decks)

        # combobox_items: List[Tuple[str, int]] = []
        # for i in range(self.count()):
        #     combobox_items.append((self.itemText(i), i))

        # if len(decks_mem.decks) == len(self.list_of_decks):
        #     return
        
        # if len(decks_mem.decks) > len(self.list_of_decks):

        #     for deck in decks_mem.decks:
        #         if deck not in self.list_of_decks:
        #             self.list_of_decks.append(deck)
        #             self.addItem(deck)

        # else:
        #     # remove from list nonexistent decks in db
        #     combobox_items: List[Tuple[str, int]] = []
        #     for i in range(self.count()):
        #         combobox_items.append((self.itemText(i), i))

        #     for i in range(len(combobox_items)):
        #         if combobox_items[i][0] not in decks_mem.decks:
        #             self.removeItem(i)
        #     # for deck in self.list_of_decks:
        #     #     if deck not in decks_mem.decks:
        #     #         self.removeItem(self)


    def mousePressEvent(self, event: QMouseEvent):
        """
        Overrides default implementation to detect clicks. It runs
        self.add_decks()
        """
        if event.button() == Qt.LeftButton: # type: ignore 
            self.update_list_of_decks()


        super().mousePressEvent(event) # calls the default behavior
    