from PySide6.QtWidgets import (
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
import json
from typing import Dict, override, Tuple
from db.tag_db import TagDB
from utils.constants import PROGRAM_NAME
from db.problem_db import ProblemDB
from db.deck_db import DeckDB
from ui.ui_utils import DeckUpdReciever, ProblemsUpdReciever, TagsUpdReciever


class BrowserWindow(
    QWidget, ProblemsUpdReciever, DeckUpdReciever, TagsUpdReciever
):
    closed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f"{PROGRAM_NAME} - Browser")
        self.main_subwidgets: Dict[str, QWidget] = {}
        self.categories_selector_subwidgets: Dict[str, QWidget] = {}

        # self._add_categories_selector()
        self._add_tree_selector()
        self._add_table_widget()

        self._add_subwidgets_to_main_layout()

        self.show()

    def closeEvent(self, event: QCloseEvent, /) -> None:
        self.closed.emit(True)
        return super().closeEvent(event)

    def _add_tree_selector(self) -> None:
        qtreewidget = QTreeWidget()
        categories_selector = self.main_subwidgets.get(
            "categories_selector", None
        )
        if categories_selector is None:
            self.main_subwidgets["categories_selector"] = qtreewidget
            self._update_tree_selector()
            self.main_subwidgets["categories_selector"].itemClicked.connect(
                        self._apply_filter_from_tree_selector
                    )

    def _apply_filter_from_tree_selector(self):
        tree_selector = self.main_subwidgets["categories_selector"]
        assert isinstance(tree_selector, QTreeWidget)
        current_item = tree_selector.currentItem()
        if current_item.text(0) == "all":
            self._update_qtablewidget()
            return

        current_type_of_item = ""
        current_parent: QTreeWidgetItem = current_item.parent()
        while (True):
            if current_parent is not None:
                if current_parent.text(0) == "decks":
                    current_type_of_item = "deck"
                    break
                if current_parent.text(0) == "tags":
                    current_type_of_item = "tag"
                    break
            else:
                return # do nothing

        type_of_filter = current_type_of_item
        filter = current_item.text(0)
        self._update_qtablewidget(filter=(type_of_filter, filter))

    def _update_tree_selector(self):
        categories_selector = self.main_subwidgets.get(
            "categories_selector", None
        )
        if categories_selector is not None and isinstance(
            categories_selector, QTreeWidget
        ):
            categories_selector.clear()
            all_item = QTreeWidgetItem()
            all_item.setText(0, "all")
            decks_item = QTreeWidgetItem()
            decks_item.setText(0, "decks")
            tags_item = QTreeWidgetItem()
            tags_item.setText(0, "tags")
            categories_selector.insertTopLevelItem(0, all_item)
            categories_selector.insertTopLevelItem(1, decks_item)
            categories_selector.insertTopLevelItem(2, tags_item)

            list_of_decks = DeckDB.get_decks_all()
            for deck in sorted(list_of_decks):
                deck_item = QTreeWidgetItem()
                deck_item.setText(0, deck)
                decks_item.addChild(deck_item)

            tags = TagDB.get_all_tags()
            for tag in sorted(tags):
                tag_item = QTreeWidgetItem()
                tag_item.setText(0, tag)
                tags_item.addChild(tag_item)

    def _add_table_widget(self) -> None:
        qtablewidget = self.main_subwidgets.get("qtablewidget", None)
        table_widget = QTableWidget()
        if qtablewidget is None:
            self.main_subwidgets["qtablewidget"] = table_widget
            self._update_qtablewidget()

    def _add_subwidgets_to_main_layout(self):
        for widget in self.main_subwidgets.values():
            self.main_layout.addWidget(widget)

    @override
    def problems_updated_reciever(self) -> None:
        self._update_qtablewidget()

    @override
    def decks_updated_reciever(self) -> None:
        self._update_tree_selector()

    def _update_qtablewidget(self, filter: Tuple[str, str] | None = None):
        
        qtablewidget = self.main_subwidgets.get("qtablewidget", None)
        if qtablewidget is not None and isinstance(qtablewidget, QTableWidget):
            
            if filter is not None:
                if filter[0] == "deck":
                    problems = ProblemDB.get_problems_by_deck(filter[1])
                else:
                    problems = ProblemDB.get_all_problems()
                    # change for problems = ProblemDB.get_problems_by_tag(filter[1])
            else:
                problems = ProblemDB.get_all_problems()

            qtablewidget.clear()
            qtablewidget.setColumnCount(4)
            qtablewidget.setHorizontalHeaderLabels(
                ["question", "solution", "deck", "creation date"]
            )

            i = 0
            for problem in problems:

                qtablewidget.setRowCount(i + 1)
                deck = DeckDB.get_deck_by_id(problem["problem_deck"])
                content = json.loads(problem["problem_content"])
                date = problem["problem_creation_date"]

                qtablewidget.setItem(
                    i, 0, QTableWidgetItem(content["question"])
                )
                qtablewidget.setItem(i, 1, QTableWidgetItem(content["answer"]))
                qtablewidget.setItem(i, 2, QTableWidgetItem(deck))
                qtablewidget.setItem(i, 3, QTableWidgetItem(date))
                i += 1

    @override
    def tags_updated_reciever(self):
        self._update_tree_selector()
