from PySide6 import QtWidgets

from PySide6.QtWidgets import (
    QVBoxLayout, 
    QWidget, 
    QPushButton, 
    QApplication, 
    QTableView, 
    QHeaderView, 
    QLineEdit,
    QWidget,
)

class EditWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Note")

        layout = QVBoxLayout()

        self.edit_header = QLineEdit()
        self.edit_description = QLineEdit()

        self.commit_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        layout.addWidget(self.edit_header)
        layout.addWidget(self.edit_description)
        layout.addWidget(self.commit_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        

app = QApplication()
window = EditWindow()
window.show()
app.exec()