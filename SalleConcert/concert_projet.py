import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QDialog, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
import mysql.connector

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

        self.setWindowTitle('Connexion')
        self.username_label = QLabel('Nom d\'utilisateur:')
        self.username_edit = QLineEdit()
        self.login_button = QPushButton('Se connecter')

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_edit)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

        self.login_button.clicked.connect(self.accept)

    def get_username(self):
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
        self.username_label = QLabel()

        layout = QGridLayout()
        layout.addWidget(self.login_button, 0, 0, 1, 3, alignment=Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.username_label, 1, 0, 1, 3)
        self.seat_buttons = []

        # Connecting to MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Fetching concert names from the database
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
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == QDialog.Accepted:
            username = login_dialog.get_username()
            self.username_label.setText(f"Connecté en tant que {username}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReservationApp()
    sys.exit(app.exec_())
