from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt


class Table(QTableWidget):
    def __init__(self, data, headers, *args, selectable=False):
        QTableWidget.__init__(self, *args)

        self.data = data
        self.setHorizontalHeaderLabels(headers)

        for n, row in enumerate(self.data):
            for m, value in enumerate(row):
                item = QTableWidgetItem(value)
                if selectable is not False and m == selectable:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                else:
                    item.setFlags(Qt.ItemIsEnabled)

                item.setToolTip(value)
                self.setItem(n, m, item)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.clicked.connect(self.on_click)

    def on_click(self):
        pass
