from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QDialog, QApplication, QMessageBox
import mysql.connector
import subprocess
from login_dialog import LoginDialog
from seat_button import SeatButton
from PyQt5.QtCore import Qt
import sys
from functools import partial

class ReservationApp(QWidget):
    current_user = None  # Variable de classe pour stocker le nom de l'utilisateur connecté

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        '''
        Programme qui nous permet de faire tout l'affichage de base de notre application
        '''
        self.setWindowTitle('Réservation de Concert')
        self.showMaximized()  # Met la fenêtre à la taille de l'écran

        # --- Création de tous nos boutons ---#

        self.login_button = QPushButton('Se connecter')
        self.login_button.clicked.connect(self.show_login_dialog)

        self.create_account_button = QPushButton('Créer un compte')
        self.create_account_button.clicked.connect(self.launch_create_account_script)

        self.manage_database_button = QPushButton('Gérer la base de données')
        self.manage_database_button.clicked.connect(self.manage_database)
        self.manage_database_button.setVisible(False)

        self.username_label = QLabel()

        # ------------------------------------#

        # --- Création de tous nos layout pour placer nos boutons ---#

        layout = QGridLayout()

        layout.addWidget(self.login_button, 1, 1, 1, 5, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.create_account_button, 1, 6, 1, 5, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.manage_database_button, 1, 6, 1, 5, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.username_label, 3, 1, 1, 10)

        self.seat_buttons = []

        # -----------------------------------------------------------#

        # Connexion à la base de données
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
            seat_button.clicked.connect(partial(self.handle_concert_click, concert[0]))
            self.seat_buttons.append(seat_button)
            layout.addWidget(seat_button, row, col)

        connection.close()

        self.setLayout(layout)
        self.show()

    def show_login_dialog(self):
        '''
        Permet de lancer la fonction lorsque le bouton 'se connecter' afin de récupérer l'utilisateur dans la base
        de données. Ajout d'une vérification si c'est un admin qui est connecté sinon cela remplace le bouton
        se connecter en 'Déconnexion'
        '''
        if self.login_button.text() == 'Se connecter':
            login_dialog = LoginDialog(self)

            if login_dialog.exec_() == QDialog.Accepted:
                email = login_dialog.get_email()
                self.current_user = email  # Stocke le nom de l'utilisateur connecté pour après
                if email == 'admin@salle_concert.fr':
                    self.show_admin_controls()
                else:
                    self.username_label.setText(f"Connecté en tant que {email}")
                    self.login_button.setText('Déconnexion')
                    self.create_account_button.setVisible(False)
        else:
            self.logout()

    def show_admin_controls(self):
        '''
        Affichage de l'interface 'Admin' lorsqu'il se connecte
        '''
        self.username_label.setText("Connecté en tant qu'Admin")
        self.login_button.setText('Déconnexion')
        self.create_account_button.setVisible(False)
        self.manage_database_button.setVisible(True)

    def manage_database(self):
        '''
        Lancer la gestion d'admin
        '''
        subprocess.run(['python3', '/home/etudiant/Documents/SAE_Prog/SalleConcert/SalleConcert/gestion_graphique/main.py'])

    def launch_create_account_script(self):
        '''
        Lancer le script de création de compte
        '''
        subprocess.run(['python3', '/home/etudiant/Documents/SAE_Prog/SalleConcert/SalleConcert/application/creation_compte.py'])

    def logout(self):
        '''
        Permet la déconnexion d'un utilisateur lorsque ce derniers est connecté
        '''
        self.username_label.clear()
        self.login_button.setText('Se connecter')
        self.create_account_button.setVisible(True)
        self.manage_database_button.setVisible(False)

    def handle_concert_click(self, concert_name):
        '''
        Fonction appelée lorsqu'un bouton de concert est cliqué
        '''
        if self.login_button.text() == 'Déconnexion':
            print(f"Concert {concert_name} is clicked by {self.current_user}.")
        else:
            QMessageBox.warning(self, 'Erreur', 'Vous devez être connecté !')
