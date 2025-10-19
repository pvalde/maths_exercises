from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Signal
from PySide6.QtGui import QCloseEvent
import json
from typing import Dict, override
from utils.constants import PROGRAM_NAME
from db.problem_db import ProblemDB
from db.deck_db import DeckDB
from ui.ui_utils import ProblemsUpdReciever


class BrowserWindow(
    QWidget, ProblemsUpdReciever
):  # TODO: should be problem upd reciever
    closed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)
        self.setWindowTitle(f"{PROGRAM_NAME} - Browser")
        self.main_subwidgets: Dict[str, QWidget] = {}

        self._add_categories_selector()
        self._add_table_widget()

        self._add_subwidgets_to_main_layout()

        self.show()

    def closeEvent(self, event: QCloseEvent, /) -> None:
        self.closed.emit(True)
        return super().closeEvent(event)

    def _add_categories_selector(self) -> None:
        """
        Configures the categories selector for BrowserWindow.
        """
        pass

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

    def _update_qtablewidget(self):
        qtablewidget = self.main_subwidgets.get("qtablewidget", None)
        if qtablewidget is not None and isinstance(qtablewidget, QTableWidget):
            qtablewidget.clear()
            qtablewidget.setColumnCount(4)
            qtablewidget.setHorizontalHeaderLabels(
                ["question", "solution", "deck", "creation date"]
            )

            problems = ProblemDB.get_all_problems()

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
