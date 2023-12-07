import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os 
import mysql.connector


class SeatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Salle de concert')
        self.selected_seats = []
        self.setGeometry(100, 100, 400, 400)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for i in range(5):
            for j in range(5):
                seat_btn = QPushButton(f"{chr(65 + i)}-{j + 1}")
                pixmap = QPixmap('../images/siege.png')
                pixmap = pixmap.scaledToWidth(50)
                icon = QIcon(pixmap)
                seat_btn.setIcon(icon)
                seat_btn.setIconSize(pixmap.size())
                seat_btn.setCheckable(True)  
                seat_btn.clicked.connect(self.on_seat_selected) 
                grid_layout.addWidget(seat_btn, i, j)

        validate_btn = QPushButton("Valider")
        validate_btn.clicked.connect(self.save_selected_seats)  # Connecter le bouton Valider à la méthode pour enregistrer les sièges
        grid_layout.addWidget(validate_btn, 6, 0, 1, 5)  # Ajouter le bouton Valider en bas
        self.show()

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

        try:
            # Connexion à la base de données MySQL
            connection = mysql.connector.connect(
                host='localhost',
                user='admin',
                password='admin',
                database='salle_concert'
            )

            cursor = connection.cursor()

            # Insertion des sièges sélectionnés dans la table MySQL
            for seat in self.selected_seats:
                cursor.execute("INSERT INTO spectateurs (emplacement) VALUES (%s)", (seat,))
            
            connection.commit()
            connection.close()

            QMessageBox.information(self, "Information", "Sièges enregistrés avec succès!")

        except mysql.connector.Error as e:
            print("Erreur lors de l'enregistrement des sièges :", e)
            QMessageBox.critical(self, "Erreur", "Erreur lors de l'enregistrement des sièges!")
    


def main():
    app = QApplication(sys.argv)
    current_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(os.path.join(current_directory, "..", "images"))
    seat_window = SeatWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()