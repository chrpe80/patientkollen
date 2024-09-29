from PySide6 import QtWidgets, QtCore
import pandas as pd
import re
from all_headers import samsa_header


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

        text_box = QtWidgets.QTextEdit()
        text_box.setToolTip("Kopiera alla personnummer från SAMSA och klistra in här separerade med kommatecken")
        button = QtWidgets.QPushButton("Skicka")
        button.clicked.connect(lambda: self.button_clicked(text_box.toPlainText()))

        container.layout().addWidget(QtWidgets.QLabel("Ta bort utskrivna - SAMSA"))
        container_layout.addWidget(text_box)
        container_layout.addWidget(button)

        self.layout.addWidget(container)

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
            updated_df.to_csv("samsa.csv", index=False, encoding="latin1")
            self.reset_form()
        else:
            pass

    def reset_form(self):
        container = self.layout.itemAt(0).widget()
        container.layout().itemAt(1).clear()




