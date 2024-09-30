from PySide6 import QtWidgets, QtCore
import pandas as pd
from blank_page import BlankPage
from table import create_table, refill_table_with_data
from all_headers import *


class VPLAddPage(BlankPage):
    def __init__(self, path="vpl.csv", layout=QtWidgets.QVBoxLayout(), columns=vpl_header):
        super().__init__(path, layout, columns)
        self._df_staff = self.load_data("staff.csv", staff_header)
        self.add_widgets()

    @property
    def df_staff(self):
        return self._df_staff

    @df_staff.setter
    def df_staff(self, value):
        self._df_staff = value

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        personal_nr_label = QtWidgets.QLabel("Personnummer (ååmmdd-xxxx)")
        personal_nr = QtWidgets.QLineEdit()

        fname_label = QtWidgets.QLabel("Förnamn")
        fname = QtWidgets.QLineEdit()

        lname_label = QtWidgets.QLabel("Efternamn")
        lname = QtWidgets.QLineEdit()

        attending_label = QtWidgets.QLabel("Tar")
        attending = QtWidgets.QComboBox()
        attending_values = [f"{item[1]} {item[2]}" for item in self.df.itertuples()]
        attending_values.insert(0, "")
        attending.addItems(attending_values)

        in_tes_label = QtWidgets.QLabel("Inlagd i TES")
        in_tes = QtWidgets.QComboBox()
        in_tes_values = ["", "Ja", "Nej"]
        in_tes.addItems(in_tes_values)

        date_label = QtWidgets.QLabel("Datum")
        date = QtWidgets.QDateEdit()
        date.setDate(QtCore.QDate.fromString("2000-01-01", "yyyy-MM-dd"))

        time_label = QtWidgets.QLabel("Tid")
        time = QtWidgets.QTimeEdit()
        time.setTime(QtCore.QTime.fromString("00:00", "hh:mm"))

        place_label = QtWidgets.QLabel("Plats")
        place = QtWidgets.QLineEdit()

        note_label = QtWidgets.QLabel("Anteckning")
        note = QtWidgets.QTextEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(
            lambda: self.button_clicked([personal_nr.text(), fname.text().title().strip(), lname.text().title().strip(),
                                         attending.currentText(), in_tes.currentText(),
                                         date.date().toString(QtCore.Qt.ISODate),
                                         time.time().toString("HH:mm"), place.text().capitalize().strip(),
                                         note.toPlainText().capitalize().strip()]))

        widgets = (
            personal_nr_label,
            personal_nr,
            fname_label,
            fname,
            lname_label,
            lname,
            attending_label,
            attending,
            in_tes_label,
            in_tes,
            date_label,
            date,
            time_label,
            time,
            place_label,
            place,
            note_label,
            note,
            button,
        )

        for widget in widgets:
            container_layout.addWidget(widget)

        self.layout.addWidget(QtWidgets.QLabel("VPL - Lägg till patient"))
        self.layout.addWidget(container)

    def update_page(self):
        self.df_staff = self.load_data("staff.csv", staff_header)
        container = self.layout.itemAt(1).widget()
        attending = container.layout().itemAt(7).widget()
        attending.clear()
        attending_values = [f"{item[1]} {item[2]}" for item in self.df_staff.itertuples()]
        attending_values.insert(0, "")
        attending.addItems(attending_values)

    @QtCore.Slot()
    def button_clicked(self, values: list):
        result = self.validate_format_personal_nr(values[0])
        match result:
            case True:
                self.save_row_to_file(self.path, self.columns, values)
                self.reset_form()
            case False:
                pass


class VPLDeletePage(BlankPage):
    def __init__(self, path="vpl.csv", layout=QtWidgets.QVBoxLayout(), columns=vpl_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        name_of_person_label = QtWidgets.QLabel("Namn")
        name_of_person = QtWidgets.QComboBox()
        name_of_person_values = [f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()]
        name_of_person.addItems(name_of_person_values)

        button = QtWidgets.QPushButton("Radera")
        button.clicked.connect(lambda: self.button_clicked(name_of_person.currentIndex()))

        widgets = name_of_person_label, name_of_person

        for widget in widgets:
            container_layout.addWidget(widget)

        container_layout.addWidget(QtWidgets.QLabel())
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("VPL - Radera patient"))
        self.layout.addWidget(container)
        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(1).widget()
        name_of_person = container.layout().itemAt(1).widget()
        name_of_person.clear()
        name_of_person.addItems([f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()])

    @QtCore.Slot()
    def button_clicked(self, index):
        df = self.load_data(self.path, self.columns)
        df = df.drop(index)
        self.save_dataframe_to_file(df)
        self.update_page()
        self.reset_form()


class VPLUpdatePage(BlankPage):
    def __init__(self, path="vpl.csv", layout=QtWidgets.QVBoxLayout(), columns=vpl_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    @staticmethod
    def validate_date_input(date_string):
        try:
            pd.to_datetime(date_string, format="%Y-%m-%d", errors='raise')
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_time_input(time_string):
        try:
            pd.to_datetime(time_string, format="%H:%M", errors='raise')
            return True
        except ValueError:
            return False

    def format_string(self, column: str, string_to_format: str):
        match column:
            case "Personnummer":
                return string_to_format

            case "Datum":
                result = self.validate_date_input(string_to_format)
                if result:
                    return string_to_format
                return "2000-01-01"

            case "Tid":
                result = self.validate_time_input(string_to_format)
                if result:
                    return string_to_format
                return "00:00"

            case "Förnamn" | "Efternamn" | "Tar" | "Inlagd_TES":
                return string_to_format.title().strip()

            case "Plats" | "Anteckning":
                return string_to_format.capitalize().strip()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        name_of_person_label = QtWidgets.QLabel("Namn")
        name_of_person = QtWidgets.QComboBox()
        name_of_person.addItems([f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()])

        column_label = QtWidgets.QLabel("Kolumn")
        column = QtWidgets.QComboBox()
        column.addItems(self.columns)

        text_field_label = QtWidgets.QLabel("Nytt värde")
        text_field = QtWidgets.QLineEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(
            lambda: self.button_clicked((name_of_person.currentIndex(), column.currentText(),
                                         self.format_string(self.columns, text_field.text()))))

        widgets = (name_of_person_label, name_of_person, column_label, column, text_field_label, text_field)

        for widget in widgets:
            container_layout.addWidget(widget)

        container_layout.addWidget(QtWidgets.QLabel())
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("VPL - Uppdatera enskild cell"))
        self.layout.addWidget(container)
        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(1).widget()
        name_of_person = container.layout().itemAt(1).widget()
        name_of_person.clear()
        name_of_person.addItems([f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()])

    @QtCore.Slot()
    def button_clicked(self, values: tuple):
        index, column, new_value = values
        if column == "Personnummer":
            result = self.validate_format_personal_nr(new_value)
            if result:
                self.df.at[index, column] = new_value
                self.save_dataframe_to_file(self.df)
                self.update_page()
                self.reset_form()
            else:
                pass
        else:
            self.df.at[index, column] = new_value
            self.save_dataframe_to_file(self.df)
            self.update_page()
            self.reset_form()


class VPLDisplayPage(BlankPage):
    def __init__(self, path="vpl.csv", layout=QtWidgets.QVBoxLayout(), columns=vpl_header):
        super().__init__(path, layout, columns)

        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        table = create_table(self.df)

        sort_values_by_personal_nr = QtWidgets.QPushButton("Personnummer")
        sort_values_by_personal_nr.clicked.connect(lambda: self.button_clicked(0))

        sort_values_by_firstname = QtWidgets.QPushButton("Förnamn")
        sort_values_by_firstname.clicked.connect(lambda: self.button_clicked(1))

        sort_values_by_lastname = QtWidgets.QPushButton("Efternamn")
        sort_values_by_lastname.clicked.connect(lambda: self.button_clicked(2))

        sort_values_by_attending = QtWidgets.QPushButton("Tar")
        sort_values_by_attending.clicked.connect(lambda: self.button_clicked(3))

        sort_values_by_in_tes = QtWidgets.QPushButton("Inlagd TES")
        sort_values_by_in_tes.clicked.connect(lambda: self.button_clicked(4))

        sort_values_by_date_time = QtWidgets.QPushButton("Datum och tid")
        sort_values_by_date_time.clicked.connect(lambda: self.button_clicked(5))

        buttons = (
            sort_values_by_personal_nr, sort_values_by_firstname, sort_values_by_lastname, sort_values_by_attending,
            sort_values_by_in_tes, sort_values_by_date_time)

        button_container = QtWidgets.QHBoxLayout()

        for b in buttons:
            button_container.addWidget(b)

        container_layout.addWidget(table)
        container_layout.addLayout(button_container)

        self.layout.addWidget(QtWidgets.QLabel("VPL - Visa"))
        self.layout.addWidget(container)

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        refill_table_with_data(self)

    @QtCore.Slot()
    def button_clicked(self, index):
        match index:
            case 0:
                self.df = self.df.sort_values("Personnummer")
                refill_table_with_data(self)
            case 1:
                self.df = self.df.sort_values("Förnamn")
                refill_table_with_data(self)
            case 2:
                self.df = self.df.sort_values("Efternamn")
                refill_table_with_data(self)
            case 3:
                self.df = self.df.sort_values(["Tar", "Datum"])
                refill_table_with_data(self)
            case 4:
                self.df = self.df.sort_values(["Inlagd TES", "Tar", "Datum"])
                refill_table_with_data(self)
            case 5:
                self.df = self.df.sort_values(["Datum", "Tid"])
                refill_table_with_data(self)


class VPL(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.vpl_add_page = VPLAddPage()
        self.vpl_delete_page = VPLDeletePage()
        self.vpl_update_page = VPLUpdatePage()
        self.vpl_display_page = VPLDisplayPage()
        self.add_tabs()

    def add_tabs(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.vpl_add_page, 'Lägg till')
        tabs.addTab(self.vpl_delete_page, 'Radera')
        tabs.addTab(self.vpl_update_page, 'Uppdatera')
        tabs.addTab(self.vpl_display_page, 'Visa')

        tabs.tabBarClicked.connect(lambda i: self.tabs_clicked(i))

        self.layout.addWidget(tabs)

    @QtCore.Slot()
    def tabs_clicked(self, i):
        match i:
            case 0:
                pass
            case 1:
                self.vpl_delete_page.update_page()
            case 2:
                self.vpl_update_page.update_page()
            case 3:
                self.vpl_display_page.update_page()
