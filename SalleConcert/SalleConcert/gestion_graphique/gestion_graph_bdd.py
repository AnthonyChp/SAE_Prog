import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QTabWidget, QTextEdit, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHBoxLayout
import mysql.connector

#from modification_spectateurs_bdd import modification_spec_bdd

class DatabaseAdminWindow(QMainWindow):
    def __init__(self):
        super(DatabaseAdminWindow, self).__init__()

        self.setWindowTitle("Database Admin Tool")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget(self.central_widget)

        self.spectateurs_tab = QWidget()
        self.concerts_tab = QWidget()

        self.tab_widget.addTab(self.spectateurs_tab, "Spectateurs")
        self.tab_widget.addTab(self.concerts_tab, "Concerts")

        self.setup_spectateurs_tab()
        self.setup_concerts_tab()

        self.layout.addWidget(self.tab_widget)


        self.connect_database()  # Connect to the database

        self.refresh_data()  # Load initial data

        self.layout.addWidget(self.tab_widget)

    def connect_database(self):
        try:
            # Replace with your database information
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="admin",
                password="admin",
                database="salle_concert"
            )

            self.cursor = self.db_connection.cursor()
            print("Connected to the database")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def closeEvent(self, event):
        # Close the database connection when the application is closed
        self.cursor.close()
        self.db_connection.close()

    def refresh_data(self):
        # Call this method to refresh data in both tabs
        self.refresh_spectateurs_data()
        self.refresh_concerts_data()

    def refresh_spectateurs_data(self):
        try:
            self.cursor.execute("SELECT * FROM spectateurs")
            data = self.cursor.fetchall()

            self.spectateurs_table.setRowCount(0)

            for row_num, row_data in enumerate(data):
                self.spectateurs_table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.spectateurs_table.setItem(row_num, col_num, item)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def refresh_concerts_data(self):
        try:
            self.cursor.execute("SELECT * FROM concerts")
            data = self.cursor.fetchall()

            self.concerts_table.setRowCount(0)

            for row_num, row_data in enumerate(data):
                self.concerts_table.insertRow(row_num)
                for col_num, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.concerts_table.setItem(row_num, col_num, item)

        except mysql.connector.Error as err:
            print(f"Error: {err}")



    def setup_spectateurs_tab(self):
        layout = QVBoxLayout(self.spectateurs_tab)

        # Display table
        self.spectateurs_table = QTableWidget()
        self.spectateurs_table.setColumnCount(10)
        self.spectateurs_table.setHorizontalHeaderLabels(["ID", "Nom", "Prenom", "Num Tel", "Email", "Mot de Passe", "ID Concert", "Nb Place Achete", "Emplacement", "Tarif"])
        layout.addWidget(self.spectateurs_table)

        # Buttons for actions
        button_layout = QHBoxLayout()

        self.refresh_spectateurs_button = QPushButton("Refresh")
        self.edit_spectateur_button = QPushButton("Edit")
        self.delete_spectateur_button = QPushButton("Delete")

        button_layout.addWidget(self.refresh_spectateurs_button)
        button_layout.addWidget(self.edit_spectateur_button)
        button_layout.addWidget(self.delete_spectateur_button)

        layout.addLayout(button_layout)

        # Shell-like window
        self.shell_output = QTextEdit()
        self.shell_output.setReadOnly(True)
        layout.addWidget(self.shell_output)

        # Connect edit button to function
        self.edit_spectateur_button.clicked.connect(self.edit_spectateur)

    def setup_concerts_tab(self):
        layout = QVBoxLayout(self.concerts_tab)

        # Display table
        self.concerts_table = QTableWidget()
        self.concerts_table.setColumnCount(5)
        self.concerts_table.setHorizontalHeaderLabels(["ID", "Titre", "Artiste", "Date", "Tarif"])
        layout.addWidget(self.concerts_table)

        # Buttons for actions
        button_layout = QHBoxLayout()

        self.refresh_concerts_button = QPushButton("Refresh")
        self.edit_concert_button = QPushButton("Edit")
        self.delete_concert_button = QPushButton("Delete")

        button_layout.addWidget(self.refresh_concerts_button)
        button_layout.addWidget(self.edit_concert_button)
        button_layout.addWidget(self.delete_concert_button)

        layout.addLayout(button_layout)

        # Shell-like window
        self.shell_output = QTextEdit()
        self.shell_output.setReadOnly(True)
        layout.addWidget(self.shell_output)

        # Connect edit button to function
        self.edit_concert_button.clicked.connect(self.edit_concert)

    def edit_spectateur(self):
        selected_row = self.spectateurs_table.currentRow()
        if selected_row >= 0:
            id_spectateur = int(self.spectateurs_table.item(selected_row, 0).text())

            # Retrieve current values
            current_values = [self.spectateurs_table.item(selected_row, col_num).text()
                              for col_num in range(self.spectateurs_table.columnCount())]

            # Create and show the edit dialog
            edit_dialog = modification_spec_bdd(id_spectateur)  # Passer l'ID ici
            result = edit_dialog.exec_()

            # Si l'utilisateur clique sur "Save" dans la boîte de dialogue
            if result == QDialog.Accepted:
                # Refresh the data
                self.refresh_spectateurs_data()

    def edit_concert(self):
        selected_row = self.concerts_table.currentRow()
        if selected_row >= 0:
            id_concert = int(self.concerts_table.item(selected_row, 0).text())

            # Retrieve current values
            current_values = [self.concerts_table.item(selected_row, col_num).text()
                              for col_num in range(self.concerts_table.columnCount())]

            # Create and show the edit dialog
            edit_dialog = EditDialog(["ID", "Titre", "Artiste", "Date", "Tarif"],
                                     current_values, self)
            result = edit_dialog.exec_()

            # If the user clicks "Save" in the dialog
            if result == QDialog.Accepted:
                edited_values = edit_dialog.get_edited_values()

                # Here, you would implement the code to update the database with the edited values
                update_query = """
                    UPDATE concerts
                    SET titre = %s, artiste = %s, date = %s, tarif = %s
                    WHERE id = %s
                """
                self.cursor.execute(update_query, (*edited_values, id_concert))
                self.db_connection.commit()

                # Print the edited values to the shell output
                self.shell_output.append(f"Editing Concert ID {id_concert} with new values: {edited_values}")

                # Refresh the data
                self.refresh_concerts_data()

def main():
    app = QApplication(sys.argv)
    window = DatabaseAdminWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
