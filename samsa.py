import pandas as pd
from PySide6 import QtWidgets, QtCore
import re
from blank_page import BlankPage
from table import create_table, refill_table_with_data
from all_headers import *
from settings import *


class SamsaAddPage(BlankPage):
    def __init__(self, path="samsa.csv", layout=QtWidgets.QVBoxLayout(), columns=samsa_header):
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
        container.setFixedWidth(fixed_width)

        personal_nr_label = QtWidgets.QLabel("Personnummer (ååmmdd-xxxx)")
        personal_nr = QtWidgets.QLineEdit()

        fname_label = QtWidgets.QLabel("Förnamn")
        fname = QtWidgets.QLineEdit()

        lname_label = QtWidgets.QLabel("Efternamn")
        lname = QtWidgets.QLineEdit()

        ot_label = QtWidgets.QLabel("AT")
        df_ots = self.df_staff[self.df_staff["Yrkestitel"] == "AT"]
        ot = QtWidgets.QComboBox()
        ot_values = [f"{item[1]} {item[2]}" for item in df_ots.itertuples()]
        ot_values.insert(0, "")
        ot.addItems(ot_values)

        pt_label = QtWidgets.QLabel("FT")
        df_pts = self.df_staff[self.df_staff["Yrkestitel"] == "FT"]
        pt = QtWidgets.QComboBox()
        pt_values = [f"{item[1]} {item[2]}" for item in df_pts.itertuples()]
        pt_values.insert(0, "")
        pt.addItems(pt_values)

        enrolled_label = QtWidgets.QLabel("Inskriven")
        enrolled = QtWidgets.QComboBox()
        enrolled.addItems(["", "Ja", "Nej"])

        tes_label_at = QtWidgets.QLabel("Inlagd i TES - AT")
        tes_at = QtWidgets.QComboBox()
        tes_at.addItems(["", "Ja", "Nej"])

        tes_label_ft = QtWidgets.QLabel("Inlagd i TES - FT")
        tes_ft = QtWidgets.QComboBox()
        tes_ft.addItems(["", "Ja", "Nej"])

        note_label = QtWidgets.QLabel("Anteckning")
        note = QtWidgets.QTextEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(lambda: self.button_clicked(
            [personal_nr.text(), fname.text().title().strip(), lname.text().title().strip(),
             ot.currentText(), pt.currentText(), enrolled.currentText(),
             tes_at.currentText(), tes_ft.currentText(),
             note.toPlainText().capitalize().strip()]))

        widgets = (
            personal_nr_label,
            personal_nr,
            fname_label,
            fname,
            lname_label,
            lname,
            ot_label,
            ot,
            pt_label,
            pt,
            enrolled_label,
            enrolled,
            tes_label_at,
            tes_at,
            tes_label_ft,
            tes_ft,
            note_label,
            note,
            button,
        )

        for widget in widgets:
            container_layout.addWidget(widget)

        self.layout.addWidget(QtWidgets.QLabel("SAMSA - Lägg till patient"), alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(container, alignment=QtCore.Qt.AlignCenter)

    def update_page(self):
        self.df_staff = self.load_data("staff.csv", staff_header)
        df_ots = self.df_staff[self.df_staff["Yrkestitel"] == "AT"]
        df_pts = self.df_staff[self.df_staff["Yrkestitel"] == "FT"]
        container = self.layout.itemAt(1).widget()
        ot = container.layout().itemAt(7).widget()
        ot.clear()
        ot_values = [f"{item[1]} {item[2]}" for item in df_ots.itertuples()]
        ot_values.insert(0, "")
        ot.addItems(ot_values)
        pt = container.layout().itemAt(9).widget()
        pt_values = [f"{item[1]} {item[2]}" for item in df_pts.itertuples()]
        pt_values.insert(0, "")
        pt.clear()
        pt.addItems(pt_values)

    @QtCore.Slot()
    def button_clicked(self, values: list):
        result = self.validate_format_personal_nr(values[0])
        match result:
            case True:
                self.save_row_to_file(self.path, samsa_header, values)
                self.reset_form()
            case False:
                pass


class SamsaDeletePage(BlankPage):
    def __init__(self, path="samsa.csv", layout=QtWidgets.QVBoxLayout(), columns=samsa_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)
        container.setFixedWidth(fixed_width)

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

        self.layout.addWidget(QtWidgets.QLabel("SAMSA - Radera patient"), alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(container, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(1).widget()
        name_of_person = container.layout().itemAt(1).widget()
        name_of_person.clear()
        name_of_person_values = [f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()]
        name_of_person.addItems(name_of_person_values)

    @QtCore.Slot()
    def button_clicked(self, index):
        if index >= 0:
            df = self.load_data(self.path, samsa_header)
            df = df.drop(index)
            self.save_dataframe_to_file(df)
            self.update_page()
            self.reset_form()
        else:
            pass


class SamsaUpdatePage(BlankPage):
    def __init__(self, path="samsa.csv", layout=QtWidgets.QVBoxLayout(), columns=samsa_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    @staticmethod
    def format_string(column: str, string_to_format: str):
        match column:
            case "Personnummer":
                return string_to_format.strip()
            case "Förnamn" | "Efternamn" | "AT" | "FT" | "Inskriven" | "Inlagd_TES_AT" | "Inlagd_TES_FT":
                return string_to_format.title().strip()
            case "Anteckning":
                return string_to_format.capitalize().strip()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)
        container.setFixedWidth(fixed_width)

        name_of_person_label = QtWidgets.QLabel("Namn")
        name_of_person = QtWidgets.QComboBox()
        name_of_person_values = [f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()]
        name_of_person.addItems(name_of_person_values)

        column_label = QtWidgets.QLabel("Kolumn")
        column = QtWidgets.QComboBox()
        column.addItems(self.columns)

        text_field_label = QtWidgets.QLabel("Nytt värde")
        text_field = QtWidgets.QLineEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(
            lambda: self.button_clicked(
                (name_of_person.currentIndex(), column.currentText(),
                 self.format_string(column.currentText(), text_field.text()))))

        widgets = (name_of_person_label, name_of_person, column_label, column, text_field_label, text_field)

        for widget in widgets:
            container_layout.addWidget(widget)

        container_layout.addWidget(QtWidgets.QLabel())
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("SAMSA - Uppdatera enskild cell"), alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(container, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch()

    def update_page(self):
        self.df = self.load_data(self.path, self.columns)
        container = self.layout.itemAt(1).widget()
        name_of_person = container.layout().itemAt(1).widget()
        name_of_person.clear()
        name_of_person_values = [f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()]
        name_of_person.addItems(name_of_person_values)

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


class SamsaDisplayPage(BlankPage):
    def __init__(self, path="samsa.csv", layout=QtWidgets.QVBoxLayout(), columns=samsa_header):
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

        sort_values_by_ot = QtWidgets.QPushButton("AT")
        sort_values_by_ot.clicked.connect(lambda: self.button_clicked(3))

        sort_values_by_pt = QtWidgets.QPushButton("FT")
        sort_values_by_pt.clicked.connect(lambda: self.button_clicked(4))

        sort_values_by_enrolled = QtWidgets.QPushButton("Inskriven")
        sort_values_by_enrolled.clicked.connect(lambda: self.button_clicked(5))

        sort_values_by_in_tes_at = QtWidgets.QPushButton("Inlagd TES - AT")
        sort_values_by_in_tes_at.clicked.connect(lambda: self.button_clicked(6))

        sort_values_by_in_tes_ft = QtWidgets.QPushButton("Inlagd TES - FT")
        sort_values_by_in_tes_ft.clicked.connect(lambda: self.button_clicked(7))

        buttons = (sort_values_by_personal_nr, sort_values_by_firstname, sort_values_by_lastname, sort_values_by_ot,
                   sort_values_by_pt, sort_values_by_enrolled, sort_values_by_in_tes_at, sort_values_by_in_tes_ft)

        button_container = QtWidgets.QHBoxLayout()

        for b in buttons:
            button_container.addWidget(b)

        container_layout.addWidget(table)
        container_layout.addLayout(button_container)

        self.layout.addWidget(QtWidgets.QLabel("SAMSA - Visa"), alignment=QtCore.Qt.AlignCenter)
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
                self.df = self.df.sort_values("AT")
                refill_table_with_data(self)
            case 4:
                self.df = self.df.sort_values("FT")
                refill_table_with_data(self)
            case 5:
                self.df = self.df.sort_values("Inskriven")
                refill_table_with_data(self)
            case 6:
                self.df = self.df.sort_values(["Inlagd_TES_AT", "AT"])
                refill_table_with_data(self)
            case 7:
                self.df = self.df.sort_values(["Inlagd_TES_FT", "FT"])
                refill_table_with_data(self)


class DeleteDiff(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)
        container.setFixedWidth(fixed_width)

        text_box = QtWidgets.QTextEdit()
        text_box.setToolTip("Kopiera alla personnummer från SAMSA och klistra in här separerade med kommatecken")
        button = QtWidgets.QPushButton("Skicka")
        button.clicked.connect(lambda: self.button_clicked(text_box.toPlainText()))

        container_layout.addWidget(text_box)
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("SAMSA - Ta bort utskrivna"), alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(container, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch()

    @staticmethod
    def load_data(path: str, columns: list):
        try:
            df = pd.read_csv(path, encoding="latin_1")
        except pd.errors.EmptyDataError:
            columns = columns
            empty_df = pd.DataFrame(columns=columns)
            empty_df.to_csv(path, index=False)
            df = pd.read_csv(path)
        return df

    @staticmethod
    def check_personal_number_format(personal_numbers):
        pattern = re.compile(r"^\d{6}-\d{4}$")

        return all(pattern.match(num) for num in personal_numbers)

    @QtCore.Slot()
    def button_clicked(self, personal_numbers: str):
        personal_numbers = personal_numbers.strip().replace(" ", "").split(sep=",")
        result = self.check_personal_number_format(personal_numbers)
        if result:
            old = set(self.load_data("samsa.csv", samsa_header)["Personnummer"].tolist())
            new = set(personal_numbers)
            diff = old.difference(new)
            old_df = self.load_data("samsa.csv", samsa_header)
            updated_df = old_df[~old_df["Personnummer"].isin(diff)]
            updated_df.to_csv("samsa.csv", index=False, encoding="latin_1")
            self.reset_form(diff, new.difference(old))
        else:
            pass

    def reset_form(self, removed_patients, new_patients):
        container = self.layout.itemAt(0).widget()
        text_box = container.layout().itemAt(1).widget()
        text_box.clear()
        text_box.insertPlainText(
            f"Nya patienter i SAMSA: {", ".join(new_patients)}\nUtskrivna: {", ".join(removed_patients)}")


class Samsa(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.samsa_add_page = SamsaAddPage()
        self.samsa_delete_page = SamsaDeletePage()
        self.samsa_update_page = SamsaUpdatePage()
        self.samsa_display_page = SamsaDisplayPage()
        self.samsa_delete_diff_page = DeleteDiff()
        self.add_tabs()

    def add_tabs(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.samsa_add_page, 'Lägg till')
        tabs.addTab(self.samsa_delete_page, 'Radera')
        tabs.addTab(self.samsa_update_page, 'Uppdatera')
        tabs.addTab(self.samsa_display_page, 'Visa')
        tabs.addTab(self.samsa_delete_diff_page, "Ta bort utskrivna")

        tabs.tabBarClicked.connect(lambda i: self.tabs_clicked(i))

        self.layout.addWidget(tabs)

    @QtCore.Slot()
    def tabs_clicked(self, i):
        match i:
            case 0:
                pass
            case 1:
                self.samsa_delete_page.update_page()
            case 2:
                self.samsa_update_page.update_page()
            case 3:
                self.samsa_display_page.update_page()
