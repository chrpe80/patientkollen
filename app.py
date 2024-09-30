from PySide6 import QtWidgets, QtCore
import sys
import csv
import os
from staff_page import StaffPage
from short_term_facilities_page import ShortTermFacilitiesPage
from samsa import Samsa
from vpl import VPL
from korttid import Korttid
from overview import OverView
from all_headers import *


class Window(QtWidgets.QMainWindow):
    """Creates the main application window"""

    def __init__(self):
        super().__init__()
        self.create_files()

        self.samsa_instance = Samsa()
        self.vpl_instance = VPL()
        self.korttid_instance = Korttid()
        self.overview_instance = OverView()

        self.staff_page_instance = StaffPage()
        self.short_term_facilities_page_instance = ShortTermFacilitiesPage()

        self.setWindowTitle("Patientkoll")
        self.setGeometry(0, 0, 1000, 600)

        self.central_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.menu_bar = self.menuBar()
        self.create_menu()
        self.init_ui()

    @staticmethod
    def create_files():
        if not os.path.exists("staff.csv"):
            with open("staff.csv", "w", encoding="latin_1") as file1:
                writer = csv.writer(file1, lineterminator="\n")
                writer.writerow(staff_header)

        if not os.path.exists("short_term_facilities.csv"):
            with open("short_term_facilities.csv", "w", encoding="latin_1") as file2:
                writer = csv.writer(file2, lineterminator="\n")
                writer.writerow(short_term_facilities_header)

        if not os.path.exists("samsa.csv"):
            with open("samsa.csv", "w", encoding="latin_1") as file3:
                writer = csv.writer(file3, lineterminator="\n")
                writer.writerow(samsa_header)

        if not os.path.exists("vpl.csv"):
            with open("vpl.csv", "w", encoding="latin_1") as file4:
                writer = csv.writer(file4, lineterminator="\n")
                writer.writerow(vpl_header)

        if not os.path.exists("korttid.csv"):
            with open("korttid.csv", "w", encoding="latin1") as file5:
                writer = csv.writer(file5, lineterminator="\n")
                writer.writerow(korttid_header)

    def create_menu(self):
        pages_menu = self.menu_bar.addMenu('Sidor')
        pages_menu.triggered.connect(self.pages_menu_triggered)
        edit_menu = self.menu_bar.addMenu("Hantera")

        # Add pages to pages_menu
        samsa = pages_menu.addAction("Samsa")
        samsa.triggered.connect(lambda: self.show_page(0))

        vpl = pages_menu.addAction("VPL")
        vpl.triggered.connect(lambda: self.show_page(1))

        korttid = pages_menu.addAction("Korttid")
        korttid.triggered.connect(lambda: self.show_page(2))

        overview = pages_menu.addAction("Översikt")
        overview.triggered.connect(lambda: self.show_page(3))

        # Add pages to edit_menu
        staff_page_action = edit_menu.addAction("Personal")
        staff_page_action.triggered.connect(lambda: self.show_page(4))

        short_term_facilities_page_action = edit_menu.addAction("Korttidsboenden")
        short_term_facilities_page_action.triggered.connect(lambda: self.show_page(5))

    def init_ui(self):
        self.central_widget.addWidget(self.samsa_instance)
        self.central_widget.addWidget(self.vpl_instance)
        self.central_widget.addWidget(self.korttid_instance)
        self.central_widget.addWidget(self.overview_instance)
        self.central_widget.addWidget(self.staff_page_instance)
        self.central_widget.addWidget(self.short_term_facilities_page_instance)

    def show_page(self, index):
        match index:
            case 0:
                self.central_widget.setCurrentIndex(0)
            case 1:
                self.central_widget.setCurrentIndex(1)
            case 2:
                self.central_widget.setCurrentIndex(2)
            case 3:
                self.central_widget.setCurrentIndex(3)
            case 4:
                self.central_widget.setCurrentIndex(4)
            case 5:
                self.central_widget.setCurrentIndex(5)

    @QtCore.Slot()
    def pages_menu_triggered(self):
        self.samsa_instance.samsa_add_page.update_page()
        self.samsa_instance.samsa_delete_page.update_page()
        self.samsa_instance.samsa_update_page.update_page()

        self.vpl_instance.vpl_add_page.update_page()
        self.vpl_instance.vpl_delete_page.update_page()
        self.vpl_instance.vpl_update_page.update_page()

        self.korttid_instance.korttid_add_page.update_page()
        self.korttid_instance.korttid_delete_page.update_page()
        self.korttid_instance.korttid_update_page.update_page()

        self.overview_instance.update_page()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Window()
    window.show()
    app.exec()
