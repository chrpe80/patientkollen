from PySide6 import QtWidgets, QtCore

from all_headers import short_term_facilities_header
from blank_page import BlankPage


def get_header():
    header = ("name", "ward")
    return header


class ShortTermFacilitiesPage(BlankPage):
    def __init__(self, path="short_term_facilities.csv", layout=QtWidgets.QVBoxLayout(), columns=short_term_facilities_header):
        super().__init__(path, layout, columns)

        self.add_widgets()

    def add_widgets(self):
        container1 = QtWidgets.QGroupBox()
        container1_layout = QtWidgets.QVBoxLayout()
        container1.setLayout(container1_layout)

        container2 = QtWidgets.QGroupBox()
        container2_layout = QtWidgets.QVBoxLayout()
        container2.setLayout(container2_layout)

        name_label = QtWidgets.QLabel("Namn")
        name = QtWidgets.QLineEdit()

        save_short_term_facility_button = QtWidgets.QPushButton("Spara")
        save_short_term_facility_button.clicked.connect(
            lambda: self.save_short_term_facility_button_clicked(name.text()))

        delete_short_term_facility_label = QtWidgets.QLabel("Ta bort")
        short_term_facilities = QtWidgets.QComboBox()
        short_term_facilities.addItems([item[1] for item in self.df.itertuples()])

        delete_short_term_facilities_button = QtWidgets.QPushButton("Ta bort")
        delete_short_term_facilities_button.clicked.connect(
            lambda: self.delete_short_term_facility_button_clicked(short_term_facilities.currentIndex()))

        widgets1 = (
            name_label,
            name,
            QtWidgets.QLabel(),
            save_short_term_facility_button,
        )

        widgets2 = (
            delete_short_term_facility_label,
            short_term_facilities,
            QtWidgets.QLabel(),
            delete_short_term_facilities_button,
        )

        for widget in widgets1:
            container1_layout.addWidget(widget)

        for widget in widgets2:
            container2_layout.addWidget(widget)

        self.layout.addWidget(QtWidgets.QLabel("Lägg till korttidsboende"))
        self.layout.addWidget(container1)
        self.layout.addWidget(QtWidgets.QLabel("Radera korttidsboende"))
        self.layout.addWidget(container2)

        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(3).widget()
        short_term_facilities = container.layout().itemAt(1).widget()
        short_term_facilities.clear()
        short_term_facilities.addItems([f"{item[1]}" for item in self.df.itertuples()])

    @QtCore.Slot()
    def save_short_term_facility_button_clicked(self, name):
        self.save_row_to_file(self.path, (name,))
        self.update_page()
        self.reset_form()

    @QtCore.Slot()
    def delete_short_term_facility_button_clicked(self, index):
        df = self.load_data(self.path, ["name_of_facility"])
        df = df.drop(index)
        self.save_dataframe_to_file(df)
        self.update_page()
        self.reset_form()
