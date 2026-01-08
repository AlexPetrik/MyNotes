import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PySide6.QtWidgets import (
    QVBoxLayout, 
    QWidget, 
    QApplication, 
    QTableView, 
    QHeaderView, 
    QLineEdit,
)
from PySide6.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

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
        # data = get_data()
        
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("mynotes.db")
        self.db.open()

        # self.model = TableModel(data)
        self.model = QSqlTableModel()
        self.initializedModel()
        
        self.table = QTableView()


        self.table.setModel(self.model)
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

        self.source_model = self.model
        self.proxy_model = QSortFilterProxyModel(self.source_model)
        self.proxy_model.setSourceModel(self.source_model)
        self.table.setModel(self.proxy_model)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search...")
        self.search_field.textChanged.connect(self.search_field.update)
        self.search_field.textChanged.connect(self.proxy_model.setFilterRegularExpression)
        self.search_field.setObjectName(u"searchcommands")
        self.search_field.setAlignment(Qt.AlignLeft)        
        reg_exp = QRegularExpression(self.search_field.text(), QRegularExpression.CaseInsensitiveOption)
        self.proxy_model.setFilterRegularExpression(
            reg_exp
        )
        self.proxy_model.setFilterKeyColumn(-1)


        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def initializedModel(self):
        self.model.setTable("notes")
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Header")
        self.model.setHeaderData(2, Qt.Horizontal, "Description")
        self.model.setHeaderData(3, Qt.Horizontal, "created_at")

    def filter_table(self, text):
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and text.lower() in item.text().lower():
                    show_row = True
                    break
                
            self.table.setRowHidden(row, not show_row)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())