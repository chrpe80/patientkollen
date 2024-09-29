from PySide6 import QtWidgets, QtCore

from all_headers import staff_header
from blank_page import BlankPage
import csv


def get_header():
    header = ("fname", "lname", "profession")
    return header


class StaffPage(BlankPage):
    def __init__(self, path="staff.csv", layout=QtWidgets.QVBoxLayout(), columns=staff_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    def add_widgets(self):
        container1 = QtWidgets.QGroupBox()
        container1_layout = QtWidgets.QVBoxLayout()
        container1.setLayout(container1_layout)

        container2 = QtWidgets.QGroupBox()
        container2_layout = QtWidgets.QVBoxLayout()
        container2.setLayout(container2_layout)

        fname_label = QtWidgets.QLabel("Förnamn")
        fname = QtWidgets.QLineEdit()

        lname_label = QtWidgets.QLabel("Efternamn")
        lname = QtWidgets.QLineEdit()

        profession_label = QtWidgets.QLabel("Yrkestitel")
        profession = QtWidgets.QComboBox()
        profession.addItems(["", "AT", "FT", "SSK"])

        save_staff_button = QtWidgets.QPushButton("Spara")
        save_staff_button.clicked.connect(
            lambda: self.save_staff_button_clicked(fname.text(), lname.text(), profession.currentText()))

        staff_label = QtWidgets.QLabel("Personal")
        staff = QtWidgets.QComboBox()
        staff_values = [f"{item[1]}, {item[2]}" for item in self.df.itertuples()]
        staff_values.insert(0, "")
        staff.addItems(staff_values)

        delete_staff_button = QtWidgets.QPushButton("Ta bort")
        delete_staff_button.clicked.connect(lambda: self.delete_staff_button_clicked(staff.currentIndex()))

        widgets1 = (
            fname_label,
            fname,
            lname_label,
            lname,
            profession_label,
            profession,
            QtWidgets.QLabel(),
            save_staff_button,
        )

        widgets2 = (
            staff_label,
            staff,
            QtWidgets.QLabel(),
            delete_staff_button,
        )

        for widget in widgets1:
            container1_layout.addWidget(widget)

        for widget in widgets2:
            container2_layout.addWidget(widget)

        self.layout.addWidget(QtWidgets.QLabel("Lägg till personal"))
        self.layout.addWidget(container1)
        self.layout.addWidget(QtWidgets.QLabel("Radera personal"))
        self.layout.addWidget(container2)

        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(3).widget()
        staff = container.layout().itemAt(1).widget()
        staff.clear()
        staff_values = [f"{item[1]}, {item[2]}" for item in self.df.itertuples()]
        staff_values.insert(0, "")
        staff.addItems(staff_values)

    @QtCore.Slot()
    def save_staff_button_clicked(self, fname, lname, profession):
        self.save_row_to_file(self.path, (fname, lname, profession))
        self.update_page()
        self.reset_form()

    @QtCore.Slot()
    def delete_staff_button_clicked(self, index):
        df = self.load_data(self.path, ["fname", "lname", "profession"])
        df = df.drop(index)
        self.save_dataframe_to_file(df)
        self.update_page()
        self.reset_form()
