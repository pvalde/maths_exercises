from PySide6.QtWidgets import QDialog

class AddDeckPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Deck")
