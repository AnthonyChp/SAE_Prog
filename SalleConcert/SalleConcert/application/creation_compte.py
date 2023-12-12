"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Lancement de la fenêtre de création de compte

.. moduleauthor:: Chapus Anthony <anthony.chapus1002@etu.univ-poitiers.fr>

"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QVBoxLayout, QLabel, QLineEdit
import mysql.connector
import bcrypt

class RegistrationApp(QWidget):
    """
    Cette classe permet à l'utilisateur de saisir les informations nécessaires pour créer un compte,
    puis d'envoyer ces informations à une base de données après un processus de hachage du mot de passe.

    :ivar nom_label: Étiquette pour le champ de saisie du nom.
    :vartype nom_label: QLabel
    :ivar nom_edit: Champ de saisie du nom.
    :vartype nom_edit: QLineEdit
    :ivar prenom_label: Étiquette pour le champ de saisie du prénom.
    :vartype prenom_label: QLabel
    :ivar prenom_edit: Champ de saisie du prénom.
    :vartype prenom_edit: QLineEdit
    :ivar num_tel_label: Étiquette pour le champ de saisie du numéro de téléphone.
    :vartype num_tel_label: QLabel
    :ivar num_tel_edit: Champ de saisie du numéro de téléphone.
    :vartype num_tel_edit: QLineEdit
    :ivar email_label: Étiquette pour le champ de saisie de l'adresse e-mail.
    :vartype email_label: QLabel
    :ivar email_edit: Champ de saisie de l'adresse e-mail.
    :vartype email_edit: QLineEdit
    :ivar password_label: Étiquette pour le champ de saisie du mot de passe.
    :vartype password_label: QLabel
    :ivar password_edit: Champ de saisie du mot de passe avec masquage.
    :vartype password_edit: QLineEdit
    :ivar register_button: Bouton pour créer un compte.
    :vartype register_button: QPushButton

    :example:

    .. code-block:: python

        registration_app = RegistrationApp()
        registration_app.show()
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Création de Compte')
        self.setGeometry(100, 100, 400, 200)

        self.nom_label = QLabel('Nom:')
        self.nom_edit = QLineEdit()

        self.prenom_label = QLabel('Prénom:')
        self.prenom_edit = QLineEdit()

        self.num_tel_label = QLabel('Numéro de téléphone:')
        self.num_tel_edit = QLineEdit()

        self.email_label = QLabel('Adresse e-mail:')
        self.email_edit = QLineEdit()

        self.password_label = QLabel('Mot de passe:')
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Créer un compte')
        self.register_button.clicked.connect(self.register_user)

        layout = QGridLayout()
        layout.addWidget(self.nom_label, 0, 0)
        layout.addWidget(self.nom_edit, 0, 1)
        layout.addWidget(self.prenom_label, 1, 0)
        layout.addWidget(self.prenom_edit, 1, 1)
        layout.addWidget(self.num_tel_label, 2, 0)
        layout.addWidget(self.num_tel_edit, 2, 1)
        layout.addWidget(self.email_label, 3, 0)
        layout.addWidget(self.email_edit, 3, 1)
        layout.addWidget(self.password_label, 4, 0)
        layout.addWidget(self.password_edit, 4, 1)
        layout.addWidget(self.register_button, 5, 0, 1, 2)

        self.setLayout(layout)

    def register_user(self):
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        num_tel = self.num_tel_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()

        # Vérifier que tous les champs sont remplis
        if not nom or not prenom or not num_tel or not email or not password:
            QMessageBox.warning(self, 'Champs non remplis', 'Veuillez remplir tous les champs.')
            return

        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Insérer le nouvel utilisateur dans la base de données
        cursor.execute("INSERT INTO spectateurs (nom, prenom, num_tel, email, mot_de_passe) VALUES (%s, %s, %s, %s, %s)",
                       (nom, prenom, num_tel, email, hashed_password))

        connection.commit()
        connection.close()

        QMessageBox.information(self, 'Création de compte', 'Compte créé avec succès!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    registration_app = RegistrationApp()
    registration_app.show()
    sys.exit(app.exec_())
