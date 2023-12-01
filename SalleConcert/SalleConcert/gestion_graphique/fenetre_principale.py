import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QTabWidget, QTextEdit, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
import mysql.connector

from modif_bdd import ModifBDD
from recup_bdd import RecupBDD

class AppGestion(QMainWindow):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager

        self.setWindowTitle('Database Viewer and Editor')
        self.resize(800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Display table
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        # Buttons for actions
        self.refresh_button = QPushButton("Refresh")
        self.edit_button = QPushButton("Edit Selected Row")
        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.edit_button)

        # Connect buttons to functions
        self.refresh_button.clicked.connect(self.refresh_data)
        self.edit_button.clicked.connect(self.edit_selected_row)

        self.refresh_data()

    def refresh_data(self):
        # Fetch data from the database
        query = "SELECT * FROM spectateurs"
        data = self.data_manager.fetch_data(query)

        # Populate the table with the fetched data
        self.table.setRowCount(0)
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels([str(header[0]) for header in self.data_manager.cursor.description])

        for row_number, row_data in enumerate(data):
            self.table.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

    def edit_selected_row(self):
        selected_row = self.table.currentRow()
        if selected_row != -1:
            data_to_edit = [self.table.item(selected_row, col).text() for col in range(self.table.columnCount())]

            edit_dialog = ModifBDD(data_to_edit, self.data_manager)
            if edit_dialog.exec_():
                edited_data = edit_dialog.get_edited_data()

                # Update the database with the edited data
                update_query = "UPDATE spectateurs SET nom = %s, prenom = %s, num_tel = %s, email = %s, mot_de_passe = %s, id_concert = %s, nb_place_achete = %s, emplacement = %s, tarif = %s WHERE ID = %s"
                self.data_manager.execute_query(update_query, edited_data[1:] + [edited_data[0]])

                # Refresh the data in the table
                self.refresh_data()

