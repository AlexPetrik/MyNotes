import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTableWidget, QVBoxLayout, QWidget, QApplication, QTableView, QHeaderView

from models.table_model import TableModel
from models.data import get_data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(800, 600)

        self.setWindowTitle("My Notes")

        # data = [
        #     [1, "Title1", "Description1" * 10],
        #     [2, "Title2" * 10, "Description2"],
        #     [3, "Title3", "Description3"],
        # ]
        data = get_data()

        self.model = TableModel(data)
        
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.table.resizeColumnsToContents()

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())