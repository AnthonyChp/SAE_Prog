from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
import bcrypt

class LoginDialog(QDialog):
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
        return self.username_edit.text()
