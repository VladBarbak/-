from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize, pyqtSlot, pyqtSignal, QDateTime
from table import Table
from datetime import *

import utils
import db_manage


class ContractScene:
    def __init__(self):
        self.main = QWidget()
        self.main_layout = QGridLayout()
        self.table = None

        self.main_layout.addWidget(QLabel('Продавець'), 0, 0)
        self.main_layout.addWidget(QLabel('Постачальник'), 0, 1)

        self.seller_combobox = QComboBox()
        self.seller_combobox.clear()
        self.seller_combobox.addItem('', -1)
        sellers = db_manage.get_sellers()
        for item in sellers:
            self.seller_combobox.addItem(item['name'], item['seller_id'])

        self.provider_combobox = QComboBox()
        self.provider_combobox.clear()
        self.provider_combobox.addItem('', -1)
        providers = db_manage.get_providers()
        self.provider_combobox = QComboBox()
        for item in providers:
            self.provider_combobox.addItem(item['name'], item['provider_id'])

        self.main_layout.addWidget(self.seller_combobox, 1, 0)
        self.main_layout.addWidget(self.provider_combobox, 1, 1)

        spacer = QWidget()
        spacer.setMaximumSize(QSize(10, 20))
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.main_layout.addWidget(spacer, 3, 0, 1, 2)

        self.main_layout.addWidget(QLabel('Обрати продукт'), 4, 0, 1, 2)

        self.set_table()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.main_layout.addWidget(self.table, 5, 0, 1, 2)

        spacer = QWidget()
        spacer.setMaximumSize(QSize(10, 30))
        spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.main_layout.addWidget(spacer, 6, 0, 1, 2)

        self.main_layout.addWidget(QLabel('Кількість'), 7, 0)

        self.amount_spinbox = QSpinBox()
        self.amount_spinbox.setMinimum(5)
        self.amount_spinbox.setMaximum(100)
        self.main_layout.addWidget(self.amount_spinbox, 7, 1)

        self.main_layout.addWidget(QLabel('Графік постачання'), 8, 0, 1, 2)

        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDateTime(QDateTime.currentDateTime())

        self.main_layout.addWidget(self.date_edit, 9, 0, 1, 2)

        self.submit_button = QPushButton('Зареєструвати')
        self.submit_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.main_layout.addWidget(self.submit_button, 10, 1)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(spacer, 11, 0, 1, 2)

        self.submit_button.pressed.connect(self.submit)

        self.main.setLayout(self.main_layout)

    def set_table(self):
        data = db_manage.get_books_catalog()
        data, headers = utils.unit_by_field(data, 'title')
        data = utils.nested_dict_to_list(data)
        rows, cols = len(data), len(data[0])

        self.table = Table(data, headers, rows, cols, selectable=0)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.resizeRowsToContents()

    def submit(self):
        try:
            seller_id = self.seller_combobox.currentData()
            provider_id = self.provider_combobox.currentData()
            supply_interval = 14
            count = self.amount_spinbox.value()
            dateandtime = self.date_edit.text()
            book_id = self.table.selectedIndexes()[0].row()
            book_id = self.table.item(book_id, 1).text()

            if seller_id == -1: raise Exception()
            if provider_id == -1: raise Exception()

            db_manage.insert_contract(seller_id, provider_id, supply_interval, count,
                                      datetime.strptime(dateandtime, '%d.%m.%Y'), book_id)

        except Exception as err:
            print(err)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Помилка")
            msg.setInformativeText('Некоректні вхідні дані')
            msg.setWindowTitle("Помилка")
            msg.exec_()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Виконано")
            msg.setInformativeText('Договір додано до бази даних')
            msg.setWindowTitle("Виконано")
            msg.exec_()

