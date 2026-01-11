from PySide6.QtCore import (QCoreApplication, Qt)
from PySide6.QtWidgets import (QDialogButtonBox, QDialog,
    QLineEdit, QTextEdit, QVBoxLayout)

class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(274, 267)
        self.verticalLayout = QVBoxLayout(self)
        self.edit_header = QLineEdit()
        self.verticalLayout.addWidget(self.edit_header)

        self.textEdit = QTextEdit()
        self.verticalLayout.addWidget(self.textEdit)

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setContextMenuPolicy(Qt.ContextMenuPolicy.PreventContextMenu)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(False)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Dialog", u"Edit Note", None))
        self.edit_header.setPlaceholderText(QCoreApplication.translate("Dialog", u"Header", None))
        self.textEdit.setPlaceholderText(QCoreApplication.translate("Dialog", u"Description", None))

    def get_inputs(self):
        if self.exec():
            return self.edit_header.text(), self.textEdit.toPlainText()
        else:
            return None, None
    