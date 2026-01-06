from PySide6 import QtCore
from PySide6.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        
    def rowCount(self, index):
        return len(self._data)
    
    def columnCount(self, index):
        return len(self._data[0])
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return "id"
            elif section == 1:
                return "Header"
            else: 
                return "Description"
        
        if orientation == QtCore.Qt.Vertical and role == Qt.DisplayRole:
            return section + 1
