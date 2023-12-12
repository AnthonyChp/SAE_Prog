"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Lancement et vérification de l'enregistrement d'un utilisateur dans la base de donnée

.. moduleauthor:: Chapus Anthony <anthony.chapus1002@etu.univ-poitiers.fr>

"""

from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import bcrypt

class LoginDialog(QDialog):
    """
    Cette classe permet à l'utilisateur de saisir son adresse e-mail et son mot de passe,
    puis de tenter de se connecter en vérifiant les informations dans une base de données.

    :ivar username_label: Étiquette pour le champ de saisie de l'adresse e-mail.
    :vartype username_label: QLabel
    :ivar username_edit: Champ de saisie de l'adresse e-mail.
    :vartype username_edit: QLineEdit
    :ivar password_label: Étiquette pour le champ de saisie du mot de passe.
    :vartype password_label: QLabel
    :ivar password_edit: Champ de saisie du mot de passe avec masquage.
    :vartype password_edit: QLineEdit
    :ivar login_button: Bouton pour tenter la connexion.
    :vartype login_button: QPushButton

    :example:

    .. code-block:: python

        login_dialog = LoginDialog(parent_instance)
        if login_dialog.exec_() == QDialog.Accepted:
            email = login_dialog.get_email()
            # Utiliser l'adresse e-mail récupérée
    """

    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Connexion')
        self.username_label = QLabel('Adresse e-mail:')
        self.username_edit = QLineEdit()
        self.password_label = QLabel('Mot de passe:')
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton('Se connecter')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_edit)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.try_login)

    def try_login(self):
        """
        Tente de connecter l'utilisateur en vérifiant les informations dans la base de données.

        :return: Aucun
        :rtype: None
        :raises: Aucune

        :example:

        .. code-block:: python

            self.try_login()
        """
        email = self.username_edit.text()
        password = self.password_edit.text()

        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Récupération du mot de passe haché depuis la base de données
        cursor.execute("SELECT mot_de_passe FROM spectateurs WHERE email = %s", (email,))
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
            # Mot de passe correct
            self.accept()
        else:
            # Mot de passe incorrect
            QMessageBox.warning(self, 'Erreur d\'authentification', 'Adresse e-mail ou mot de passe incorrect')

        connection.close()

    def get_email(self):
        """
        Récupère l'adresse e-mail saisie par l'utilisateur.

        :return: L'adresse e-mail saisie par l'utilisateur.
        :rtype: str
        :raises: Aucune

        :example:

        .. code-block:: python

            email = self.get_email()
        """
        return self.username_edit.text()
