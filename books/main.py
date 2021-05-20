from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from catalog_scene import Catalog
from seller_scene import SellerScene
from contract_scene import ContractScene

import utils
import db_manage

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        # set the title of main window
        self.setWindowIcon(QIcon('icon.png'))
        self.setWindowTitle('Books system')

        # set the size of window
        self.Width = 1200
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)

        # add all widgets
        self.btn_1 = QPushButton('Каталог', self)
        self.btn_2 = QPushButton('Продавці', self)
        self.btn_3 = QPushButton('Скласти\nдоговір', self)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)

        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)

        left_layout.setSizeConstraint(QLayout.SetFixedSize)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, alignment=Qt.Alignment(Qt.AlignLeft | Qt.AlignTop))
        main_layout.addWidget(self.right_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # -----------------
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    # -----------------
    # pages

    def ui1(self):
        self.catalog = Catalog()
        return self.catalog.main

    def ui2(self):
        self.seller_cabinet = SellerScene()
        return self.seller_cabinet.main

    def ui3(self):
        self.contract_form = ContractScene()
        return self.contract_form.main


if __name__ == '__main__':
    from qt_material import apply_stylesheet

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_amber.xml')

    ex = Window()
    ex.show()

    app.setStyle('Fusion')
    sys.exit(app.exec_())
