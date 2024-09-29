from PySide6 import QtWidgets, QtCore
from all_headers import staff_header, short_term_facilities_header, korttid_header
from table import create_table, refill_table_with_data
from blank_page import BlankPage


class KorttidAddPage(BlankPage):
    def __init__(self, path="korttid.csv", layout=QtWidgets.QVBoxLayout(), columns=korttid_header):
        super().__init__(path, layout, columns)
        self._df_staff = self.load_data("staff.csv", staff_header)
        self._df_short_term_facilities = self.load_data("short_term_facilities.csv", short_term_facilities_header)
        self.add_widgets()

    @property
    def df_staff(self):
        return self._df_staff

    @df_staff.setter
    def df_staff(self, value):
        self._df_staff = value

    @property
    def df_short_term_facilities(self):
        return self._df_short_term_facilities

    @df_short_term_facilities.setter
    def df_short_term_facilities(self, value):
        self._df_short_term_facilities = value

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

        short_term_facility_label = QtWidgets.QLabel("Korttid")
        short_term_facility = QtWidgets.QComboBox()
        short_term_facility_values = [item[1] for item in self.df_short_term_facilities.itertuples()]
        short_term_facility_values.insert(0, "")
        short_term_facility.addItems(short_term_facility_values)

        note_label = QtWidgets.QLabel("Anteckning")
        note = QtWidgets.QTextEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(lambda: self.button_clicked((personal_nr.text(), fname.text(), lname.text(),
                                                            ot.currentText(), pt.currentText(),
                                                            short_term_facility.currentText(),
                                                            note.toPlainText())))

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
            short_term_facility_label,
            short_term_facility,
            note_label,
            note,
            button,
        )

        for widget in widgets:
            container_layout.addWidget(widget)

        self.layout.addWidget(QtWidgets.QLabel("Korttid - Lägg till patient"))
        self.layout.addWidget(container)

    def update_page(self):
        self.df_staff = self.load_data("staff.csv", staff_header)
        self.df_short_term_facilities = self.load_data("short_term_facilities.csv", short_term_facilities_header)
        df_ots = self.df_staff[self.df_staff["Yrkestitel"] == "AT"]
        df_pts = self.df_staff[self.df_staff["Yrkestitel"] == "FT"]
        container = self.layout.itemAt(1).widget()
        ot = container.layout().itemAt(7).widget()
        ot.clear()
        ot_values = [f"{item[1]} {item[2]}" for item in df_ots.itertuples()]
        ot_values.insert(0, "")
        ot.addItems(ot_values)

        pt = container.layout().itemAt(9).widget()
        pt.clear()
        pt_values = [f"{item[1]} {item[2]}" for item in df_pts.itertuples()]
        pt_values.insert(0, "")
        pt.addItems(pt_values)

        short_term_facility = container.layout().itemAt(11).widget()
        short_term_facility.clear()
        short_term_facility_values = [f"{item[1]}" for item in self.df_short_term_facilities.itertuples()]
        short_term_facility_values.insert(0, "")
        short_term_facility.addItems(short_term_facility_values)

    @QtCore.Slot()
    def button_clicked(self, values: tuple):
        result = self.validate_format_personal_nr(values[0])
        match result:
            case True:
                self.save_row_to_file(self.path, values)
                self.reset_form()
            case False:
                pass


class KorttidDeletePage(BlankPage):
    def __init__(self, path="korttid.csv", layout=QtWidgets.QVBoxLayout(), columns=korttid_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        name_of_person_label = QtWidgets.QLabel("Namn")
        name_of_person = QtWidgets.QComboBox()
        name_of_person.addItems([f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()])

        button = QtWidgets.QPushButton("Radera")
        button.clicked.connect(lambda: self.button_clicked(name_of_person.currentIndex()))

        widgets = name_of_person_label, name_of_person

        for widget in widgets:
            container_layout.addWidget(widget)

        container_layout.addWidget(QtWidgets.QLabel())
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("Korttid - Radera patient"))
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
        df = self.load_data(self.path, korttid_header)
        df = df.drop(index)
        self.save_dataframe_to_file(df)
        self.update_page()
        self.reset_form()


class KorttidUpdatePage(BlankPage):
    def __init__(self, path="korttid.csv", layout=QtWidgets.QVBoxLayout(), columns=korttid_header):
        super().__init__(path, layout, columns)
        self.add_widgets()

    def add_widgets(self):
        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QVBoxLayout()
        container.setLayout(container_layout)

        name_of_person_label = QtWidgets.QLabel("Namn")
        name_of_person = QtWidgets.QComboBox()
        name_of_person.addItems([f"{item[1]}, {item[2]} {item[3]}" for item in self.df.itertuples()])

        column_label = QtWidgets.QLabel("Kolumn")
        column = QtWidgets.QComboBox()
        column_values = korttid_header
        column_values.insert(0, "")
        column.addItems(column_values)

        text_field_label = QtWidgets.QLabel("Nytt värde")
        text_field = QtWidgets.QLineEdit()

        button = QtWidgets.QPushButton("Spara")
        button.clicked.connect(
            lambda: self.button_clicked((name_of_person.currentIndex(), column.currentText(), text_field.text())))

        widgets = (name_of_person_label, name_of_person, column_label, column, text_field_label, text_field)

        for widget in widgets:
            container_layout.addWidget(widget)

        container_layout.addWidget(QtWidgets.QLabel())
        container_layout.addWidget(button)

        self.layout.addWidget(QtWidgets.QLabel("Korttid - Uppdatera enskild cell"))
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


class KorttidDisplayPage(BlankPage):
    def __init__(self, path="korttid.csv", layout=QtWidgets.QVBoxLayout(), columns=korttid_header):
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

        sort_values_by_short_term_facility = QtWidgets.QPushButton("Korttid")
        sort_values_by_short_term_facility.clicked.connect(lambda: self.button_clicked(5))

        buttons = (
            sort_values_by_personal_nr, sort_values_by_firstname, sort_values_by_lastname, sort_values_by_ot,
            sort_values_by_pt, sort_values_by_short_term_facility)

        button_container = QtWidgets.QHBoxLayout()

        for b in buttons:
            button_container.addWidget(b)

        container_layout.addWidget(table)
        container_layout.addLayout(button_container)

        self.layout.addWidget(QtWidgets.QLabel("Korttid - Visa"))
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
                self.df = self.df.sort_values("Korttid")
                refill_table_with_data(self)


class Korttid(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.korttid_add_page = KorttidAddPage()
        self.korttid_delete_page = KorttidDeletePage()
        self.korttid_update_page = KorttidUpdatePage()
        self.korttid_display_page = KorttidDisplayPage()
        self.add_tabs()

    def add_tabs(self):
        tabs = QtWidgets.QTabWidget()
        tabs.addTab(self.korttid_add_page, 'Lägg till')
        tabs.addTab(self.korttid_delete_page, 'Radera')
        tabs.addTab(self.korttid_update_page, 'Uppdatera')
        tabs.addTab(self.korttid_display_page, 'Visa')

        tabs.tabBarClicked.connect(lambda i: self.tabs_clicked(i))

        self.layout.addWidget(tabs)

    @QtCore.Slot()
    def tabs_clicked(self, i):
        match i:
            case 0:
                pass
            case 1:
                self.korttid_delete_page.update_page()
            case 2:
                self.korttid_update_page.update_page()
            case 3:
                self.korttid_display_page.update_page()
