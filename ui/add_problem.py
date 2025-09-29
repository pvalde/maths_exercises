import re
from typing import override

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCloseEvent, QFont, QFontMetrics, QMouseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QComboBox,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from db.deck_db import DeckDB
from db.problem_db import ProblemDB
from ui.ui_utils import NoInternetProfile, DeckUpdReciever

# CONSTANTS
from utils.constants import (
    MAIN_DIR,
    MATHJAX3_PATH,
    PROGRAM_NAME,
    USER_MEDIA_QURL,
)


class AddProblemWindow(QWidget, DeckUpdReciever):
    """
    Window for adding new 'exercises' to the database.
    """

    closed = Signal(bool)
    problem_added = Signal(bool)

    def __init__(self):
        """ """
        super().__init__()
        self.setWindowTitle(f"{PROGRAM_NAME} - Add New")

        layout = QVBoxLayout()

        # Deck selection --------------------------------
        self.deckSelectorTitle = QLabel("Deck")
        self.deck_selector = DeckSelector()

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
        layout.addWidget(self.deck_selector)

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
            content=content, deck=self.deck_selector.currentText()
        )
        print(f"new problem added to '{self.deck_selector.currentText()}'!!!")
        self.problem_added.emit(True)
        self.closed.emit(True)
        self.close()

    def closeEvent(self, event: QCloseEvent, /) -> None:
        print(f"front: '{self.front_edit.toPlainText()}'")
        print(f"back: '{self.back_edit.toPlainText()}'")
        if not (
            re.fullmatch(r"\s*", self.front_edit.toPlainText())
            and re.fullmatch(r"\s*", self.back_edit.toPlainText())
        ):
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Discard current input?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.html_view_cleanup()
                self.closed.emit(True)
                event.accept()

            else:
                event.ignore()

        else:
            self.closed.emit(True)
            self.html_view_cleanup()

    def html_view_cleanup(self):
        self.html_viewer.stop()
        # self.html_viewer.loadFinished.disconnect() # not necessary
        page = self.html_viewer.page()
        if page:
            page.deleteLater()
        QTimer.singleShot(
            0, lambda: self.html_viewer.deleteLater()
        )  # give some time to delete the WebEnginePage Object before the QWebEngineView One

    @override
    def decks_updated_reciever(self):
        self.deck_selector.decks_updated_reciever()


class DeckSelector(QComboBox, DeckUpdReciever):
    def __init__(self):
        super().__init__()

        self.update_list_of_decks()

    def update_list_of_decks(self):
        """
        Checks if the decks table in the db has been modified. If true, update
        the DeckSelector's list of decks according to that.
        """
        # delete the current list in DeckSelector class
        n_of_items = self.count()
        for i in range(n_of_items):
            self.removeItem(n_of_items - 1 - i)

        print("DeckSelector retrieving list of decks from DB.")
        self.addItems(sorted(DeckDB.get_decks_all()))

    def mousePressEvent(self, event: QMouseEvent):
        """
        Overrides default implementation to detect clicks. It runs
        self.add_decks()
        """
        if event.button() == Qt.LeftButton:  # type: ignore
            self.update_list_of_decks()

        super().mousePressEvent(event)  # calls the default behavior

    @override
    def decks_updated_reciever(self):
        self.update_list_of_decks()
