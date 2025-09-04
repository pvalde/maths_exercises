from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Maths Exercises')

        container = QWidget()
        self.setCentralWidget(container)

        container_layout = QVBoxLayout(container)
        label1 = QLabel("Label 1")
        label2 = QLabel("Label 2")

        container_layout.addWidget(label1)
        container_layout.addWidget(label2)


        #Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        #Exit QAction
        self.file_menu.addAction("Exit", self.close)


def initializeGui():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()


