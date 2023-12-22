import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import mysql.connector
import os
from login_dialog import LoginDialog

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

        current_directory = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_directory, '..' ,'..','images', 'siege.png')

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for i in range(5):
            for j in range(5):
                seat_btn = QPushButton(f"{chr(65 + i)}-{j + 1}")

                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaledToWidth(50)
                seat_btn.setIcon(QIcon(pixmap))
                seat_btn.setIconSize(pixmap.size())

                seat_btn.setCheckable(True)  
                seat_btn.clicked.connect(self.on_seat_selected) 
                grid_layout.addWidget(seat_btn, i, j)

        validate_btn = QPushButton("Valider")
        validate_btn.clicked.connect(self.save_selected_seats)  
        grid_layout.addWidget(validate_btn, 6, 0, 1, 5)  

        self.show()

    def set_current_user(self, current_user):
        self.current_user = current_user

    def on_seat_selected(self):
        seat_btn = self.sender()

        if seat_btn.isChecked():
            seat_btn.setStyleSheet("border: 2px solid green;")
            seat_name = seat_btn.text()
            if seat_name not in self.selected_seats:
                self.selected_seats.append(seat_name)
        else:
            seat_btn.setStyleSheet("")
            seat_name = seat_btn.text()
            if seat_name in self.selected_seats:
                self.selected_seats.remove(seat_name)

        print("Sièges sélectionnés :", self.selected_seats)

    def save_selected_seats(self):
        if not self.selected_seats:
            QMessageBox.warning(self, "Avertissement", "Aucun siège sélectionné!")
            return

        if not self.current_user:
            QMessageBox.warning(self, "Avertissement", "Utilisateur non identifié!")
            return

        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )

        cursor = connection.cursor()

        try:
            selected_seat = self.selected_seats[0]

            print(self.current_user)

            sql = 'INSERT INTO spectateurs (emplacement) VALUES (%s)'
            values = (selected_seat,)
            cursor.execute(sql, values)

            connection.commit()
            print(cursor.rowcount, "lignes insérées.")
            QMessageBox.information(self, "Information", "Siège enregistré avec succès!")

        except mysql.connector.Error as err:
            print("Error:", err)
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'enregistrement du siège:\n{err}")

        finally:
            connection.close()

def main():
    app = QApplication(sys.argv)
    seat_window = SeatWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
