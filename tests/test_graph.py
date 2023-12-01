import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QDialog, QLabel, QLineEdit
import mysql.connector

class DataManager:
    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="salle_concert"
        )
        self.cursor = self.db_connection.cursor()

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_query(self, query, data):
        self.cursor.execute(query, data)
        self.db_connection.commit()


class DatabaseViewer(QMainWindow):
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

            edit_dialog = EditDialog(data_to_edit, self.data_manager)
            if edit_dialog.exec_():
                edited_data = edit_dialog.get_edited_data()

                # Update the database with the edited data
                update_query = "UPDATE spectateurs SET nom = %s, prenom = %s, num_tel = %s, email = %s, mot_de_passe = %s, id_concert = %s, nb_place_achete = %s, emplacement = %s, tarif = %s WHERE ID = %s"
                self.data_manager.execute_query(update_query, edited_data[1:] + [edited_data[0]])

                # Refresh the data in the table
                self.refresh_data()


class EditDialog(QDialog):
    def __init__(self, data_to_edit, data_manager):
        super().__init__()
        self.data_manager = data_manager

        self.setWindowTitle('Edit Row')
        self.resize(300, 200)

        self.layout = QVBoxLayout(self)

        # Display labels and line edits for each column
        self.line_edits = []
        for label, value in zip(["ID", "Nom", "Prenom", "Num Tel", "Email", "Mot de Passe", "ID Concert", "Nb Place Achete", "Emplacement", "Tarif"], data_to_edit):
            label_widget = QLabel(label)
            line_edit = QLineEdit(value)

            self.layout.addWidget(label_widget)
            self.layout.addWidget(line_edit)

            self.line_edits.append(line_edit)

        # Button to confirm the edits
        self.confirm_button = QPushButton("Confirm Edit")
        self.layout.addWidget(self.confirm_button)

        # Connect the button to the function
        self.confirm_button.clicked.connect(self.accept)

    def get_edited_data(self):
        return [line_edit.text() for line_edit in self.line_edits]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    data_manager = DataManager()
    window = DatabaseViewer(data_manager)
    window.show()
    sys.exit(app.exec_())
