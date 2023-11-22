import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QDialog, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector
import bcrypt
import subprocess

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


class SeatButton(QPushButton):
    def __init__(self, row, col, concert_name):
        super().__init__(concert_name)
        self.row = row
        self.col = col
        self.clicked.connect(self.reserve_seat)

    def reserve_seat(self):
        if self.text() == "Réservé":
            QMessageBox.warning(self, "Déjà réservé", f"Le siège {self.row+1}-{self.col+1} est déjà réservé.")
        else:
            self.setText("Réservé")
            QMessageBox.information(self, "Réservation", f"Siège {self.row+1}-{self.col+1} réservé avec succès!")


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
        layout.addWidget(self.login_button, 0, 0, 1, 3, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.create_account_button, 0, 3, 1, 3, alignment=Qt.AlignTop | Qt.AlignRight)
        layout.addWidget(self.username_label, 1, 0, 1, 6)
        self.seat_buttons = []

        # Connexion à la base de donnée
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Permet de récupérer les concert de la base de donnée
        cursor.execute("SELECT titre FROM concerts")
        concerts = cursor.fetchall()

        # Adding seat buttons with concert names
        for i, concert in enumerate(concerts):
            row = i // 3 + 2
            col = i % 3
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
        subprocess.run(['python3', 'creation_compte.py'])

    def logout(self):
        self.username_label.clear()
        self.login_button.setText('Se connecter')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReservationApp()
    sys.exit(app.exec_())
