import re
from typing import override, List

from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QCloseEvent, QFont, QFontMetrics, QMouseEvent
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLayoutItem,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    # QTextEdit,
    QLineEdit,
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


class TagSelectorWidget(QWidget):
    """
    Interactive tags selector.
    """

    def __init__(self):
        self.n_of_items: int = 0

        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Label
        self.label = QLabel("Tags")
        layout.addWidget(self.label)

        # tags container
        self.tags_container = QWidget()
        self.tags_container_layout = QVBoxLayout()
        self.tags_container.setLayout(self.tags_container_layout)

        # new tag button
        self.add_new_tag_button = QPushButton("+")
        self.add_new_tag_button.setMaximumWidth(25)
        self.add_new_tag_button.clicked.connect(
            lambda: self._add_new_tag(self.tags_container_layout)
        )
        layout.addWidget(self.tags_container)
        layout.addWidget(
            self.add_new_tag_button, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        # self.remove_tag_button = QPushButton("-")

    def _add_new_tag(self, tags_container_layout: QLayout) -> None:
        """
        Adds a new QLayoutItem object to tags_container_layout. The first
        contains a QWidget object with QHBoxLayout that contains QLineEdit
        and QPushButton objects.
        """
        # create new tag entry
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        text_input = QLineEdit()
        text_input.setMaximumHeight(25)
        remove_button = QPushButton("-")
        remove_button.setMaximumWidth(25)
        remove_button.clicked.connect(
            lambda: self._remove_tag(tags_container_layout, widget)
        )

        layout.addWidget(text_input)
        layout.addWidget(remove_button)

        tags_container_layout.addWidget(widget)

    def _remove_tag(
        self, tags_container_layout: QLayout, tag_widget: QWidget
    ) -> None:
        """
        Removes tag_widget from tags_container_layout by removing the
        QLayoutItem object that contains the tag_widget.
        """
        if tags_container_layout is not None:
            for i in range(tags_container_layout.count()):
                q_layout_item: QLayoutItem | None = (
                    tags_container_layout.itemAt(i)
                )
                if q_layout_item is not None:
                    if q_layout_item.widget() == tag_widget:
                        tags_container_layout.removeItem(q_layout_item)

    def remove_all_tags(self):
        for i in range(self.tags_container_layout.count() - 1, -1, -1):
            q_layout_item: QLayoutItem | None = (
                self.tags_container_layout.itemAt(i)
            )
            if q_layout_item is None:
                pass
            else:
                self.tags_container_layout.removeItem(q_layout_item)

    def tags(self) -> List[str]:
        """
        Returns a list of strings containing all the tags added. If a tag is
        whitespace only, it is ignored. If no tags has been added, an empty
        list is returned.
        """
        tags: List[str] = []
        count = range(
            self.tags_container_layout.count() - 1,
        )
        for i in count:
            q_layout_item: QLayoutItem | None = (
                self.tags_container_layout.itemAt(i)
            )
            if q_layout_item is not None:
                q_line_edit_obj = q_layout_item.widget().children()[1]
                assert q_line_edit_obj is not None
                if isinstance(q_line_edit_obj, QLineEdit):
                    tag = q_line_edit_obj.text().strip()
                    if tag.isspace() is not True and len(tag) > 0:
                        tags.append(tag)

        return tags


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

        # tags selector
        self.tags_selector = TagSelectorWidget()

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

        # -- tags selector ----------------
        layout.addWidget(self.tags_selector)

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

        self.html_viewer.setHtml(html_content, baseUrl=USER_MEDIA_QURL)
        self.html_viewer.update()

    def add_problem(self) -> None:
        content = {
            "question": self.front_edit.toPlainText(),
            "answer": self.back_edit.toPlainText(),
        }
        tags = self.tags_selector.tags()
        if len(tags) > 0:
            ProblemDB.add_deck(
                content=content,
                deck=self.deck_selector.currentText(),
                tags=tags,
            )

        else:
            ProblemDB.add_deck(
                content=content, deck=self.deck_selector.currentText()
            )

        self.problem_added.emit(True)
        # clean all data:
        self.front_edit.clear()
        self.back_edit.clear()
        # self.tags_selector.remove_all_tags()
        # the previous one has been commented out because is better to keep tags for a question
        # of adding problems to the db.

        # send message to user
        QMessageBox.information(
            None, "Success", "The Problem has been succesfully added."
        )
        # self.closed.emit(True)
        # self.close()

    def closeEvent(self, event: QCloseEvent, /) -> None:
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
