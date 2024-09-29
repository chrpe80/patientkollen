from PySide6 import QtWidgets, QtCore
import pandas as pd
import csv
import re
from abc import abstractmethod


class BlankPage(QtWidgets.QWidget):
    def __init__(self, path: str, layout: QtWidgets.QLayout, columns: list) -> None:
        super().__init__()
        self._path = path
        self._columns = columns
        self._df = self.load_data(self._path, self._columns)
        self._layout = layout
        self.setLayout(self._layout)

    @property
    def path(self):
        return self._path

    @property
    def columns(self):
        return self._columns

    @property
    def df(self):
        return self._df

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def layout(self):
        return self._layout

    @staticmethod
    def load_data(path: str, columns: list):
        try:
            df = pd.read_csv(path, encoding="latin-1").fillna("Ingen info")
        except pd.errors.EmptyDataError:
            columns = columns
            empty_df = pd.DataFrame(columns=columns)
            empty_df.to_csv(path, index=False)
            df = pd.read_csv(path)
        return df

    @staticmethod
    def validate_format_personal_nr(input_string):
        pattern = r'^\d{6}-\d{4}$'

        if re.match(pattern, input_string):
            return True
        else:
            return False

    def save_dataframe_to_file(self, df):
        df.to_csv(self.path, index=False, encoding="latin1")

    def reset_form(self) -> None:
        groupbox_layout = self.layout.itemAt(1).widget().layout()
        for i in range(groupbox_layout.count()):
            if isinstance(groupbox_layout.itemAt(i).widget(), QtWidgets.QLineEdit):
                groupbox_layout.itemAt(i).widget().clear()

            elif isinstance(groupbox_layout.itemAt(i).widget(), QtWidgets.QTextEdit):
                groupbox_layout.itemAt(i).widget().clear()

            elif isinstance(groupbox_layout.itemAt(i).widget(), QtWidgets.QComboBox):
                groupbox_layout.itemAt(i).widget().setCurrentIndex(0)

            elif isinstance(groupbox_layout.itemAt(i).widget(), QtWidgets.QTimeEdit):
                groupbox_layout.itemAt(i).widget().setTime(QtCore.QTime.fromString("00:00", "hh:mm"))

            elif isinstance(groupbox_layout.itemAt(i).widget(), QtWidgets.QDateEdit):
                groupbox_layout.itemAt(i).widget().setDate(QtCore.QDate.fromString("2000-01-01", "yyyy-MM-dd"))

    @staticmethod
    def save_row_to_file(path: str, variable: tuple):
        with open(path, "a", encoding="latin1") as file:
            writer = csv.writer(file, lineterminator="\n")
            writer.writerow(variable)

    @abstractmethod
    def add_widgets(self) -> None:
        """Adds all widgets to the main page layout"""

        pass

    @abstractmethod
    def update_page(self):
        pass
