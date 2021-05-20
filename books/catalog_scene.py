from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from table import Table

import utils
import db_manage


class Catalog:
    def __init__(self):
        self.main_layout = QHBoxLayout()
        self.table = None

        right_sidebar = QWidget()
        right_sidebar.setMinimumSize(QSize(200, 200))

        right_sidebar_layout = QVBoxLayout()

        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(self.filter_handler)
        self.combobox.addItem('Усі', -1)
        categories = db_manage.get_categories()
        for item in categories:
            self.combobox.addItem(item['name'], item['category_id'])

        right_sidebar_layout.addWidget(QLabel('Фільтр за категорією:'))
        right_sidebar_layout.addWidget(self.combobox)
        right_sidebar_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.main_layout.addWidget(right_sidebar)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        right_sidebar.setLayout(right_sidebar_layout)

        self.get_full_catalog()

    def set_table(self, data, headers, rows, cols):
        if self.table is not None:
            self.main_layout.removeWidget(self.table)
            self.table.deleteLater()
            self.table = None

        self.table = Table(data, headers, rows, cols)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()

        self.main_layout.addWidget(self.table)

    def get_full_catalog(self):
        data = db_manage.get_books_catalog()
        data, headers = utils.unit_by_field(data, 'title', ['book_id'])
        data = utils.nested_dict_to_list(data)
        self.set_table(data, headers, len(data), len(data[0]))

    def filter_handler(self):
        category_id = self.combobox.currentData()

        if category_id == -1:
            self.get_full_catalog()
            return

        data = db_manage.get_books_catalog_by_category(category_id)
        data, headers = utils.unit_by_field(data, 'title', ['book_id'])
        data = utils.nested_dict_to_list(data)
        self.set_table(data, headers, len(data), len(data[0]))
