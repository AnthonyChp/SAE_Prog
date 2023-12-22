"""
.. module:: reservation_app
   :platform: Unix, Windows
   :synopsis: Confection de l'application Salle_Concert.

.. moduleauthor:: Chapus Anthony <anthony.chapus1002@etu.univ-poitiers.fr>

"""
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QDialog, QMessageBox, QApplication
import mysql.connector
import subprocess
from login_dialog import LoginDialog
from seat_button import SeatButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from functools import partial
import sys
from script_siege import SeatWindow

class ReservationApp(QWidget):
    """
    Classe principale de l'application de réservation de concerts.

    Cette classe gère l'interface utilisateur, la connexion/déconnexion des utilisateurs,
    l'affichage des informations de l'utilisateur, et l'interaction avec la base de données.

    :ivar current_user: Variable de classe pour stocker le nom de l'utilisateur connecté.
    :vartype current_user: str or None

    :example:

    .. code-block:: python

        app_instance = ReservationApp()
        app_instance.show()
    """
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur de l'application, mettant en place l'affichage de base.
    
        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            instance.init_ui()
        """
        self.setWindowTitle('Réservation de Concert')

        self.login_button = QPushButton('Se connecter')
        self.login_button.clicked.connect(self.show_login_dialog)

        self.create_account_button = QPushButton('Créer un compte')
        self.create_account_button.clicked.connect(self.launch_create_account_script)

        self.manage_database_button = QPushButton('Gérer la base de données')
        self.manage_database_button.clicked.connect(self.manage_database)
        self.manage_database_button.setVisible(False)

        self.username_label = QLabel()

        layout = QGridLayout()
        layout.setSpacing(50)

        row_count = 6
        layout.setRowStretch(4, 1)
        layout.setRowStretch(row_count, 1)

        layout.addWidget(self.login_button, 0, 1, 1, 5, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.create_account_button, 0, 6, 1, 5, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.manage_database_button, 0, 6, 1, 5, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.username_label, 2, 1, 1, 10)


        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        cursor.execute("SELECT id, titre, tarif FROM concerts")
        concerts = cursor.fetchall()

        layout.setRowStretch(0, 1)
        layout.setRowStretch(row_count, 1)

                # Inside the for loop where you create concert buttons
        for i, concert in enumerate(concerts):
            row = i // 3 + 1
            col = i % 3 + 1 + (3 - (len(concerts) % 3 + 1) // 2)

            concert_info = f"{concert[1]}\nTarif: {concert[2]}"
            seat_button = QPushButton(concert_info)
            layout.addWidget(seat_button, row + 2, col)

            seat_button.setFixedSize(300, 300)
            seat_button.setStyleSheet(
                '''
                QPushButton {
                    border-radius: 20px;
                    border: 2px solid black;
                }
                QPushButton:hover {
                    background-color: lightgray;
                }
                '''
            )

            # Ajout a chaque bouton sa propre fonction
            seat_button.clicked.connect(partial(self.concert_clique, concert_info))

            if concert[0] == 1:
                pixmap = QPixmap('SalleConcert/images/josman.jpg')
                pixmap = pixmap.scaledToWidth(300)
                icon = QIcon(pixmap)
                seat_button.setIcon(icon)
                seat_button.setIconSize(pixmap.size())
            elif concert[0] == 2:
                pixmap = QPixmap('SalleConcert/images/kikesa.jpg')
                pixmap = pixmap.scaledToWidth(300)
                icon = QIcon(pixmap)
                seat_button.setIcon(icon)
                seat_button.setIconSize(pixmap.size())
            else:
                pixmap = QPixmap('SalleConcert/images/ziak.jpg')
                pixmap = pixmap.scaledToWidth(300)
                icon = QIcon(pixmap)
                seat_button.setIcon(icon)
                seat_button.setIconSize(pixmap.size())

        connection.close()
        self.setLayout(layout)
        self.show()


    def show_login_dialog(self):
        """ Lance la boîte de dialogue de connexion lorsque le bouton 'Se connecter' est cliqué,
        permettant la récupération des informations de l'utilisateur depuis la base de données.
        Vérifie si l'utilisateur connecté est un administrateur et met à jour l'interface utilisateur en conséquence.
        Remplace le bouton 'Se connecter' par 'Déconnexion' si l'utilisateur n'est pas un administrateur.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

        instance.show_login_dialog()
        """
        if self.login_button.text() == 'Se connecter':
            login_dialog = LoginDialog(self)

            if login_dialog.exec_() == QDialog.Accepted:
                email = login_dialog.get_email()
                self.current_user = email
                if email == 'admin@salle_concert.fr':
                    self.show_admin_controls()
                else:
                    self.username_label.setText(f"Connecté en tant que {email}")
                    self.login_button.setText('Déconnexion')
                    self.create_account_button.setVisible(False)
        else:
            self.logout()

    def show_admin_controls(self):
        """Affiche l'interface d'administration lorsque l'administrateur se connecte.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            instance.show_admin_controls()
        """
        self.username_label.setText("Connecté en tant qu'Admin")
        self.login_button.setText('Déconnexion')
        self.create_account_button.setVisible(False)
        self.manage_database_button.setVisible(True)

    def manage_database(self):
        """Lance l'interface de gestion de la base de données pour l'administrateur.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            instance.manage_database()
        """
        subprocess.run(['python3', '/home/etudiant/Documents/SAE_Prog/SalleConcert/SalleConcert/gestion_graphique/main.py'])

    def launch_create_account_script(self):
        """Lance l'interface de création de compte dans la base de données.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            instance.manage_database()
        """
        subprocess.run(['python3', '/home/etudiant/Documents/SAE_Prog/SalleConcert/SalleConcert/application/creation_compte.py'])

    def logout(self):
        """Permet la déconnexion d'un utilisateur lorsqu'il est connecté.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            instance.logout()
        """
        self.username_label.clear()
        self.login_button.setText('Se connecter')
        self.create_account_button.setVisible(True)
        self.manage_database_button.setVisible(False)

    def concert_clique(self, concert_name):
        """Fonction appelée lorsqu'un bouton de concert est cliqué.

    :param concert_name: Le nom du concert cliqué.
    :type concert_name: str
    :return: Aucun
    :rtype: None
    :raises: Aucune

    :example:

    .. code-block:: python

        instance.concert_clique("Nom du concert")
    """
        subprocess.run(['python3', '/home/etudiant/21_12/SAE_Prog/SalleConcert/SalleConcert/application/script_siege.py'], check=True)