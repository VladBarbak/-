from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QCursor
from table import Table

import utils
import db_manage


class MenuItem(QLabel):
    clicked = pyqtSignal()

    def __init__(self, *args):
        super(MenuItem, self).__init__(*args)
        self.setStyleSheet('font-size: 14px; text-decoration: underline; cursor: pointer')
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class Cabinet(QWidget):
    def __init__(self, seller_id, set_menu, parent=None):
        super(Cabinet, self).__init__(parent)
        self.seller_id = seller_id
        self.seller_name = db_manage.get_seller_by_id(seller_id)[0]['name']
        self.set_menu = set_menu

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.main = None
        self.main_page()

        self.setLayout(self.layout)

    def show_schedule(self):
        schedule_data = db_manage.get_schedule_for_seller(self.seller_id)
        schedule_list = []
        headers = []

        for item in schedule_data:
            row = []
            for key, value in item.items():
                if key not in headers:
                    headers.append(key)

                if key == 'day':
                    value = ['Понеділок', 'Вівторок', 'Середа', 'Четвер', 'П\'ятниця', 'Субота', 'Неділя'][int(value)-1]

                row.append(str(value))
            schedule_list.append(row)

        schedule_table = Table(schedule_list, headers, len(schedule_list), len(headers))
        return schedule_table

    def show_supplying(self):
        supplying_data = db_manage.get_supplying_for_seller(self.seller_id)
        supplying_list = []
        headers = []

        for item in supplying_data:
            row = []
            for key, value in item.items():
                if key not in headers:
                    headers.append(key)

                row.append(str(value))
            supplying_list.append(row)

        supplying_table = Table(supplying_list, headers, len(supplying_list), len(headers))
        supplying_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        return supplying_table

    def show_sells(self):
        selling_data = db_manage.get_selling_of_seller(self.seller_id)
        selling_list = []
        headers = []

        for item in selling_data:
            row = []
            for key, value in item.items():
                if key not in headers:
                    headers.append(key)

                row.append(str(value))
            selling_list.append(row)

        selling_table = Table(selling_list, headers, len(selling_list), len(headers))
        selling_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        selling_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        selling_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        return selling_table

    def show_contracts(self):
        contract_data = db_manage.get_providers_for_seller(self.seller_id)
        contract_list = []
        headers = []

        for item in contract_data:
            row = []
            for key, value in item.items():
                if key not in headers:
                    headers.append(key)

                if key == 'provide interval':
                    value = 'Кожних ' + str(value) + ' дней'

                row.append(str(value))
            contract_list.append(row)

        contract_table = Table(contract_list, headers, len(contract_list), len(headers))
        return contract_table

    def remove_page(self):
        self.layout.removeWidget(self.main)
        self.main.deleteLater()
        self.main = None

    def main_page(self):
        if self.main is not None:
            self.remove_page()

        self.main = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.main.setLayout(main_layout)

        main_layout.addWidget(QLabel('Розклад роботи продавця - ' + self.seller_name))
        main_layout.addWidget(self.show_schedule())

        main_layout.addWidget(QLabel('Очікувані партії продукції'))
        main_layout.addWidget(self.show_supplying())

        self.layout.addWidget(self.main)

        sell_page_link = MenuItem('Облік проданої продукції')
        sell_page_link.clicked.connect(self.selling_page)

        contract_page_link = MenuItem('Список постачальників')
        contract_page_link.clicked.connect(self.contract_page)

        self.set_menu([
            sell_page_link,
            contract_page_link
        ])

    def selling_page(self):
        if self.main is not None:
            self.remove_page()

        self.main = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.main.setLayout(main_layout)

        main_layout.addWidget(QLabel('Облік проданої продукції продавцем - ' + self.seller_name))
        main_layout.addWidget(self.show_sells())

        self.layout.addWidget(self.main)

        schedule_link = MenuItem('Розклад')
        schedule_link.clicked.connect(self.main_page)

        contract_page_link = MenuItem('Список постачальників')
        contract_page_link.clicked.connect(self.contract_page)

        self.set_menu([
            schedule_link,
            contract_page_link
        ])

    def contract_page(self):
        if self.main is not None:
            self.remove_page()

        self.main = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.main.setLayout(main_layout)

        main_layout.addWidget(QLabel('Список договорів - ' + self.seller_name))
        main_layout.addWidget(self.show_contracts())

        self.layout.addWidget(self.main)

        schedule_link = MenuItem('Розклад')
        schedule_link.clicked.connect(self.main_page)

        sell_page_link = MenuItem('Облік проданої продукції')
        sell_page_link.clicked.connect(self.selling_page)

        self.set_menu([
            schedule_link,
            sell_page_link
        ])


class SellerScene:
    def __init__(self):
        self.main_layout = QHBoxLayout()
        self.cabinet = None
        self.menu = None

        self.right_sidebar = QWidget()
        self.right_sidebar.setMinimumSize(QSize(200, 200))

        self.right_sidebar_layout = QVBoxLayout()

        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(self.filter_handler)
        self.combobox.clear()
        self.combobox.addItem('', -1)
        sellers = db_manage.get_sellers()
        for item in sellers:
            self.combobox.addItem(item['name'], item['seller_id'])
        self.right_sidebar_layout.addWidget(QLabel('Оберіть продавця'))
        self.right_sidebar_layout.addWidget(self.combobox)
        self.right_sidebar_layout.addStretch()

        self.main_layout.addWidget(self.right_sidebar)

        self.main = QWidget()
        self.main.setLayout(self.main_layout)
        self.right_sidebar.setLayout(self.right_sidebar_layout)

    def set_cabinet(self, seller_id):
        if self.cabinet is not None:
            self.main_layout.removeWidget(self.cabinet)
            self.cabinet.deleteLater()
            self.cabinet = None

        self.cabinet = Cabinet(seller_id, self.set_menu)
        self.main_layout.addWidget(self.cabinet)

    def set_menu(self, items):
        if self.menu is not None:
            self.right_sidebar_layout.removeWidget(self.menu)
            self.menu.deleteLater()
            self.menu = None

        self.menu = QWidget()
        menu_layout = QVBoxLayout()

        for item in items:
            menu_layout.addWidget(item)

        self.menu.setLayout(menu_layout)
        self.right_sidebar_layout.insertWidget(self.right_sidebar_layout.count() -1, self.menu)

    def filter_handler(self):
        seller_id = self.combobox.currentData()

        if seller_id == -1:
            return

        self.set_cabinet(seller_id)
