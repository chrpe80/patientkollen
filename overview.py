from PySide6 import QtWidgets, QtCore
import pandas as pd
from table import create_table
from all_headers import *


class OverView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.samsa_path = "samsa.csv"
        self.vpl_path = "vpl.csv"
        self.korttid_path = "korttid.csv"

        samsa_df = self.load_data(self.samsa_path, samsa_header)
        samsa_df = samsa_df[samsa_df["Inskriven"] == "Ja"]
        self._samsa_df = samsa_df[["Förnamn", "Efternamn", "AT", "FT"]]

        self._vpl_df = self.load_data(self.vpl_path, vpl_header)[
            ["Förnamn", "Efternamn", "Tar", "Datum"]]
        self._korttid_df = self.load_data(self.korttid_path, korttid_header)[["Förnamn", "Efternamn", "AT", "FT"]]

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.add_widgets()

    @property
    def samsa_df(self):
        return self._samsa_df

    @samsa_df.setter
    def samsa_df(self, value):
        self._samsa_df = value

    @property
    def vpl_df(self):
        return self._vpl_df

    @vpl_df.setter
    def vpl_df(self, value):
        self._vpl_df = value

    @property
    def korttid_df(self):
        return self._korttid_df

    @korttid_df.setter
    def korttid_df(self, value):
        self._korttid_df = value

    @staticmethod
    def load_data(path: str, columns: list):
        try:
            df = pd.read_csv(path, encoding="latin-1")
        except pd.errors.EmptyDataError:
            columns = columns
            empty_df = pd.DataFrame(columns=columns)
            empty_df.to_csv(path, index=False)
            df = pd.read_csv(path)
        return df

    def add_widgets(self):
        samsa_layout = QtWidgets.QVBoxLayout()
        vpl_layout = QtWidgets.QVBoxLayout()
        korttid_layout = QtWidgets.QVBoxLayout()

        container = QtWidgets.QGroupBox()
        container_layout = QtWidgets.QHBoxLayout()
        container.setLayout(container_layout)

        samsa_table = create_table(self.samsa_df)
        vpl_table = create_table(self.vpl_df)
        korttid_table = create_table(self.korttid_df)

        samsa_sort_by_first = QtWidgets.QPushButton("Förnamn")
        samsa_sort_by_first.clicked.connect(lambda: self.button_clicked_samsa(0))
        samsa_sort_by_last = QtWidgets.QPushButton("Efternamn")
        samsa_sort_by_last.clicked.connect(lambda: self.button_clicked_samsa(1))
        samsa_sort_by_at = QtWidgets.QPushButton("AT")
        samsa_sort_by_at.clicked.connect(lambda: self.button_clicked_samsa(2))
        samsa_sort_by_ft = QtWidgets.QPushButton("FT")
        samsa_sort_by_ft.clicked.connect(lambda: self.button_clicked_samsa(3))

        vpl_sort_by_first = QtWidgets.QPushButton("Förnamn")
        vpl_sort_by_first.clicked.connect(lambda: self.button_clicked_vpl(0))
        vpl_sort_by_last = QtWidgets.QPushButton("Efternamn")
        vpl_sort_by_last.clicked.connect(lambda: self.button_clicked_vpl(1))
        vpl_sort_by_attending = QtWidgets.QPushButton("Tar")
        vpl_sort_by_attending.clicked.connect(lambda: self.button_clicked_vpl(2))
        vpl_sort_by_date = QtWidgets.QPushButton("Datum")
        vpl_sort_by_date.clicked.connect(lambda: self.button_clicked_vpl(3))

        korttid_sort_by_first = QtWidgets.QPushButton("Förnamn")
        korttid_sort_by_first.clicked.connect(lambda: self.button_clicked_korttid(0))
        korttid_sort_by_last = QtWidgets.QPushButton("Efternamn")
        korttid_sort_by_last.clicked.connect(lambda: self.button_clicked_korttid(1))
        korttid_sort_by_at = QtWidgets.QPushButton("AT")
        korttid_sort_by_at.clicked.connect(lambda: self.button_clicked_korttid(2))
        korttid_sort_by_ft = QtWidgets.QPushButton("FT")
        korttid_sort_by_ft.clicked.connect(lambda: self.button_clicked_korttid(3))

        samsa_button_layout = QtWidgets.QHBoxLayout()

        samsa_button_layout.addWidget(samsa_sort_by_first)
        samsa_button_layout.addWidget(samsa_sort_by_last)
        samsa_button_layout.addWidget(samsa_sort_by_at)
        samsa_button_layout.addWidget(samsa_sort_by_ft)

        vpl_button_layout = QtWidgets.QHBoxLayout()

        vpl_button_layout.addWidget(vpl_sort_by_first)
        vpl_button_layout.addWidget(vpl_sort_by_last)
        vpl_button_layout.addWidget(vpl_sort_by_attending)
        vpl_button_layout.addWidget(vpl_sort_by_date)

        korttid_button_layout = QtWidgets.QHBoxLayout()

        korttid_button_layout.addWidget(korttid_sort_by_first)
        korttid_button_layout.addWidget(korttid_sort_by_last)
        korttid_button_layout.addWidget(korttid_sort_by_at)
        korttid_button_layout.addWidget(korttid_sort_by_ft)

        samsa_layout.addWidget(QtWidgets.QLabel("SAMSA - Inskrivna"))
        samsa_layout.addWidget(samsa_table)
        samsa_layout.addLayout(samsa_button_layout)
        vpl_layout.addWidget(QtWidgets.QLabel("VPL"))
        vpl_layout.addWidget(vpl_table)
        vpl_layout.addLayout(vpl_button_layout)
        korttid_layout.addWidget(QtWidgets.QLabel("KORTTID"))
        korttid_layout.addWidget(korttid_table)
        korttid_layout.addLayout(korttid_button_layout)

        container_layout.addLayout(samsa_layout)
        container_layout.addLayout(vpl_layout)
        container_layout.addLayout(korttid_layout)

        self.layout.addWidget(container)

    def refill_table_with_data(self, container_layout_index, df):
        """Refills a table widget"""

        container = self.layout.itemAt(0).widget()
        container_layout = container.layout().itemAt(container_layout_index)

        table = container_layout.itemAt(1).widget()
        table.setRowCount(0)
        table.setRowCount(df.shape[0])
        table.setColumnCount(df.shape[1])
        table.verticalHeader().setVisible(False)

        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QtWidgets.QTableWidgetItem(str(df.iloc[i, j]))
                item.setToolTip(str(df.iloc[i, j]))
                table.setItem(i, j, item)

    def update_page(self):
        samsa_df = self.load_data(self.samsa_path, samsa_header)
        samsa_df = samsa_df[samsa_df["Inskriven"] == "Ja"]
        self.samsa_df = samsa_df[["Förnamn", "Efternamn", "AT", "FT"]]
        self.vpl_df = self.load_data(self.vpl_path, vpl_header)[["Förnamn", "Efternamn", "Tar", "Datum"]]
        self.korttid_df = self.load_data(self.korttid_path, korttid_header)[["Förnamn", "Efternamn", "AT", "FT"]]

        self.refill_table_with_data(0, self.samsa_df)
        self.refill_table_with_data(1, self.vpl_df)
        self.refill_table_with_data(2, self.korttid_df)

    @QtCore.Slot()
    def button_clicked_samsa(self, index):
        match index:
            case 0:
                self.samsa_df = self.samsa_df.sort_values("Förnamn")
                self.refill_table_with_data(0, self.samsa_df)
            case 1:
                self.samsa_df = self.samsa_df.sort_values("Efternamn")
                self.refill_table_with_data(0, self.samsa_df)
            case 2:
                self.samsa_df = self.samsa_df.sort_values("AT")
                self.refill_table_with_data(0, self.samsa_df)
            case 3:
                self.samsa_df = self.samsa_df.sort_values("FT")
                self.refill_table_with_data(0, self.samsa_df)

    @QtCore.Slot()
    def button_clicked_vpl(self, index):
        match index:
            case 0:
                self.vpl_df = self.vpl_df.sort_values("Förnamn")
                self.refill_table_with_data(1, self.vpl_df)
            case 1:
                self.vpl_df = self.vpl_df.sort_values("Efternamn")
                self.refill_table_with_data(1, self.vpl_df)
            case 2:
                self.vpl_df = self.vpl_df.sort_values("Tar")
                self.refill_table_with_data(1, self.vpl_df)
            case 3:
                self.vpl_df = self.vpl_df.sort_values(["Datum", "Förnamn", "Efternamn"])
                self.refill_table_with_data(1, self.vpl_df)

    @QtCore.Slot()
    def button_clicked_korttid(self, index):
        match index:
            case 0:
                self.korttid_df = self.korttid_df.sort_values("Förnamn")
                self.refill_table_with_data(2, self.korttid_df)
            case 1:
                self.korttid_df = self.korttid_df.sort_values("Efternamn")
                self.refill_table_with_data(2, self.korttid_df)
            case 2:
                self.korttid_df = self.korttid_df.sort_values("AT")
                self.refill_table_with_data(2, self.korttid_df)
            case 3:
                self.korttid_df = self.korttid_df.sort_values("FT")
                self.refill_table_with_data(2, self.korttid_df)
