from PySide6 import QtWidgets, QtCore
import pandas as pd
import numpy as np
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
            df = pd.read_csv(path, encoding="latin_1")
        except pd.errors.EmptyDataError:
            empty_df = pd.DataFrame(columns=columns)
            empty_df.to_csv(path, index=False, encoding="latin_1")
            df = pd.read_csv(path, encoding="latin_1")
        return df

    @staticmethod
    def validate_format_personal_nr(input_string):
        pattern = r'^\d{6}-\d{4}$'

        if re.match(pattern, input_string):
            return True
        else:
            return False

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

    def save_dataframe_to_file(self, df):
        df = df.replace("", np.nan).fillna("Ingen info").drop_duplicates()
        df.to_csv(self.path, index=False, encoding="latin_1")

    def save_row_to_file(self, path: str, keys: list, values: list):
        old_df = self.load_data(path, keys)
        index = [old_df.shape[0]]
        keys_values_zipped = zip(keys, values)
        keys_values_dict = {k: v for k, v in keys_values_zipped}
        new_row = pd.DataFrame(data=keys_values_dict, index=index)
        new_entry = pd.concat([old_df, new_row])
        self.save_dataframe_to_file(new_entry)

    @abstractmethod
    def add_widgets(self) -> None:
        pass

    @abstractmethod
    def update_page(self):
        pass
