from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QDialog
import mysql.connector
import subprocess
from login_dialog import LoginDialog
from seat_button import SeatButton
from PyQt5.QtCore import Qt

class ReservationApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Réservation de Concert')
        self.showMaximized()  # Maximize the window

        self.login_button = QPushButton('Se connecter')
        self.login_button.clicked.connect(self.show_login_dialog)
        self.create_account_button = QPushButton('Créer un compte')
        self.create_account_button.clicked.connect(self.launch_create_account_script)
        self.username_label = QLabel()

        layout = QGridLayout()


        layout.addWidget(self.login_button, 1, 1, 1, 5, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.create_account_button, 1, 6, 1, 5, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.username_label, 2, 1, 1, 10)
        self.seat_buttons = []

        # Connexion à la base de donnée
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Permet de récupérer les concerts de la base de données
        cursor.execute("SELECT titre FROM concerts")
        concerts = cursor.fetchall()

        # Ajout des boutons de siège avec les noms des concerts
        for i, concert in enumerate(concerts):
            # Calculer le nombre de lignes nécessaires pour centrer verticalement
            rows_needed = (len(concerts) - 1) // 3 + 1
            row = i // 3 + 3
            
            # Centrer horizontalement
            col = i % 3 + 1 + (3 - (len(concerts) % 3 + 1) // 2)
            
            seat_button = SeatButton(row - 2, col, concert[0])
            self.seat_buttons.append(seat_button)
            layout.addWidget(seat_button, row, col)


        connection.close()

        self.setLayout(layout)
        self.show()

    def show_login_dialog(self):
        if self.login_button.text() == 'Se connecter':
            login_dialog = LoginDialog(self)
            if login_dialog.exec_() == QDialog.Accepted:
                email = login_dialog.get_email()
                self.username_label.setText(f"Connecté en tant que {email}")
                self.login_button.setText('Déconnexion')
        else:
            self.logout()

    def launch_create_account_script(self):
        # Lancer le script de création de compte
        subprocess.run(['python3', '/home/etudiant/Documents/SAE_Prog/SalleConcert/application/creation_compte.py'])

    def logout(self):
        self.username_label.clear()
        self.login_button.setText('Se connecter')
