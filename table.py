from PySide6 import QtWidgets


def create_table(df):
    """Creates a table to display a dataframe"""

    table = QtWidgets.QTableWidget()
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(df.columns)
    table.verticalHeader().setVisible(False)
    table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
    header = table.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            item = QtWidgets.QTableWidgetItem(str(df.iloc[i, j]))
            item.setToolTip(str(df.iloc[i, j]))
            table.setItem(i, j, item)

    return table


def refill_table_with_data(instance):
    """Refills the table widget"""

    container = instance.layout.itemAt(1).widget()
    table = container.layout().itemAt(0).widget()
    table.setRowCount(0)
    table.setRowCount(instance.df.shape[0])
    table.setColumnCount(instance.df.shape[1])
    table.verticalHeader().setVisible(False)

    for i in range(instance.df.shape[0]):
        for j in range(instance.df.shape[1]):
            item = QtWidgets.QTableWidgetItem(str(instance.df.iloc[i, j]))
            item.setToolTip(str(instance.df.iloc[i, j]))
            table.setItem(i, j, item)

    return table


