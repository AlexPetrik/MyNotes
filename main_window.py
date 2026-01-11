import sys
from datetime import datetime

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSortFilterProxyModel, QRegularExpression
from PySide6.QtWidgets import (
    QVBoxLayout, 
    QHBoxLayout, 
    QWidget, 
    QApplication, 
    QTableView, 
    QHeaderView, 
    QLineEdit,
    QDialogButtonBox,
    QDialog,
)
from PySide6.QtSql import QSqlDatabase, QSqlTableModel
from edit_dialog import EditDialog


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

        button_add = QtWidgets.QPushButton("Add")
        button_add.setFixedSize(100, 30)
        button_add.clicked.connect(self.add_clicked)

        button_del= QtWidgets.QPushButton("Delete")
        button_del.setFixedSize(100, 30)
       
        buttonbox = QHBoxLayout()
        buttonbox.setContentsMargins(10, 10, 10, 10)
        buttonbox.setSpacing(10)
        buttonbox.addStretch()
        buttonbox.addWidget(button_add)
        buttonbox.addWidget(button_del)

        layout = QVBoxLayout()
        layout.addWidget(self.search_field)
        layout.addWidget(self.table)
        layout.addLayout(buttonbox)

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

    def add_clicked(self):
        dlg = EditDialog(self)

        result = dlg.exec()

        if result == QDialog.Accepted:
            header, description = dlg.get_inputs()
            if header and description:
                self.model.insertRows(self.model.rowCount(), 1)
                # self.model.setData(self.model.index(self.model.rowCount() - 1, 0), self.model.rowCount())
                self.model.setData(self.model.index(self.model.rowCount() - 1, 1), header)
                self.model.setData(self.model.index(self.model.rowCount() - 1, 2), description)
                self.model.setData(self.model.index(self.model.rowCount() - 1, 3), datetime.datetime.now())
                self.model.submitAll()
                self.model.select()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())