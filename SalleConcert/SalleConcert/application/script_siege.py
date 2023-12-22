import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from login_dialog import LoginDialog
import mysql.connector
import os

class SeatWindow(QWidget):
    def __init__(self):
        super().__init__()

        
        self.login_dialog = LoginDialog(self)
        self.current_user = None 

        if self.login_dialog.exec_() == LoginDialog.Accepted:
            self.current_user = self.login_dialog.get_email()
            print(self.current_user)
            self.initUI()
        else:
            self.logout()

    def initUI(self):
        self.setWindowTitle('Salle de concert')
        self.selected_seats = []
        self.setGeometry(100, 100, 400, 400)

        # Use absolute path to load the image
        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, 'images', 'siege.png')

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for i in range(5):
            for j in range(5):
                seat_btn = QPushButton(f"{chr(65 + i)}-{j + 1}")

                # Set the icon using absolute path
                pixmap = QPixmap(image_path)
                seat_btn.setIcon(QIcon(pixmap))
                seat_btn.setIconSize(pixmap.size())

                seat_btn.setCheckable(True)  
                seat_btn.clicked.connect(self.on_seat_selected) 
                grid_layout.addWidget(seat_btn, i, j)

        validate_btn = QPushButton("Valider")
        validate_btn.clicked.connect(self.save_selected_seats)  
        grid_layout.addWidget(validate_btn, 6, 0, 1, 5)  

        # Add QLineEdit widgets for name and email
        self.name_edit = QLineEdit()
        self.email_edit = QLineEdit()

        grid_layout.addWidget(QLabel("Nom:"), 7, 0)
        grid_layout.addWidget(self.name_edit, 7, 1, 1, 4)
        grid_layout.addWidget(QLabel("Email:"), 8, 0)
        grid_layout.addWidget(self.email_edit, 8, 1, 1, 4)

        self.show()

    def set_current_user(self, current_user):
        self.current_user = current_user

    def on_seat_selected(self):
        seat_btn = self.sender()  # Récupérer le bouton qui a déclenché le signal

        if seat_btn.isChecked():  # Vérifier si le bouton est coché (sélectionné)
            seat_btn.setStyleSheet("border: 2px solid green;")  # Changer le style du bouton
            seat_name = seat_btn.text()
            if seat_name not in self.selected_seats:
                self.selected_seats.append(seat_name)  # Ajouter le siège à la liste des sièges sélectionnés
        else:
            seat_btn.setStyleSheet("")  # Réinitialiser le style du bouton
            seat_name = seat_btn.text()
            if seat_name in self.selected_seats:
                self.selected_seats.remove(seat_name)  # Enlever le siège de la liste des sièges sélectionnés

        print("Sièges sélectionnés :", self.selected_seats)  # Afficher les sièges sélectionnés dans la console

    def save_selected_seats(self):
        if not self.selected_seats:
            QMessageBox.warning(self, "Avertissement", "Aucun siège sélectionné!")
            return

        name = self.name_edit.text()
        email = self.email_edit.text()

        if not name or not email:
            QMessageBox.warning(self, "Avertissement", "Veuillez remplir tous les champs!")
            return

        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )

        cursor = connection.cursor()

        for seat in self.selected_seats:
            sql = "INSERT INTO spectateurs (nom, email, emplacement) VALUES (%s, %s, %s)"
            values = (name, email, seat)
            cursor.execute(sql, values)

        connection.commit()
        print(cursor.rowcount, "lignes insérées.")
        connection.close()

        QMessageBox.information(self, "Information", "Sièges enregistrés avec succès!")

def main():
    app = QApplication(sys.argv)
    seat_window = SeatWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
