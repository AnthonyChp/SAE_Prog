import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateEdit, QPushButton
from PyQt5.QtCore import QDate
import sqlite3

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        date_edit = QDateEdit(self)
        date_edit.setCalendarPopup(True)  # Pour afficher un calendrier lors du clic sur le champ de date
        layout.addWidget(date_edit)

        insert_button = QPushButton("Insérer dans la base de données", self)
        insert_button.clicked.connect(lambda: self.insert_date(date_edit.date()))
        layout.addWidget(insert_button)

        self.setLayout(layout)
        self.setWindowTitle("Exemple d'insertion de date avec PyQt")

    def insert_date(self, selected_date):
        # Récupérer la date au format Python
        python_date = selected_date.toPyDate()

        # Convertir la date en format adapté à votre base de données
        # Ici, nous utilisons le format ISO (YYYY-MM-DD)
        formatted_date = python_date.isoformat()

        # Insérer la date dans la base de données (utilisation de SQLite à titre d'exemple)
        connection = sqlite3.connect('votre_base_de_donnees.db')
        cursor = connection.cursor()

        # Remplacez "table_name" et "date_column" par vos valeurs réelles
        query = f"INSERT INTO table_name (date_column) VALUES ('{formatted_date}')"
        cursor.execute(query)

        connection.commit()
        connection.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
