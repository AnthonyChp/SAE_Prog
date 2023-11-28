import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QLabel, QLineEdit
import mysql.connector


class modification_spec_bdd(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.setWindowTitle('Modification de Compte')
        self.setGeometry(100, 100, 400, 300)

        # Sauvegarder l'ID de l'utilisateur que vous souhaitez modifier
        self.user_id = user_id

        # Connexion à la base de données pour récupérer les données actuelles
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Récupération des données actuelles de l'utilisateur
        cursor.execute("SELECT * FROM spectateurs WHERE id = %s", (user_id,))
        user_data = cursor.fetchone()
        connection.close()

        # Création des champs d'édition avec les données actuelles
        self.id_label = QLabel('ID de l\'utilisateur :')
        self.id_edit = QLineEdit(str(user_data[0]))
        self.id_edit.setReadOnly(True)

        self.nom_label = QLabel('Nom :')
        self.nom_edit = QLineEdit(user_data[1]) 

        self.prenom_label = QLabel('Prénom :')
        self.prenom_edit = QLineEdit(user_data[2]) 

        self.num_tel_label = QLabel('Numéro de téléphone :')
        self.num_tel_edit = QLineEdit(str(user_data[3]))  

        self.email_label = QLabel('Adresse e-mail :')
        self.email_edit = QLineEdit(user_data[4]) 

        self.id_concert_label = QLabel('ID du Concert :')
        self.id_concert_edit = QLineEdit(str(user_data[6]))

        self.nb_place_achete_label = QLabel('Nombre de places achetées :')
        self.nb_place_achete_edit = QLineEdit(str(user_data[7]))

        self.emplacement_label = QLabel('Emplacement :')
        self.emplacement_edit = QLineEdit(str(user_data[8]))

        self.tarif_label = QLabel('Tarif :')
        self.tarif_edit = QLineEdit(str(user_data[9]))

#id nb place emplacement tarif

        self.update_button = QPushButton('Modifier le compte')
        self.update_button.clicked.connect(self.update_user)

        layout = QGridLayout()
        layout.addWidget(self.id_label, 0, 0)
        layout.addWidget(self.id_edit, 0, 1)
        layout.addWidget(self.nom_label, 1, 0)
        layout.addWidget(self.nom_edit, 1, 1)
        layout.addWidget(self.prenom_label, 2, 0)
        layout.addWidget(self.prenom_edit, 2, 1)
        layout.addWidget(self.num_tel_label, 3, 0)
        layout.addWidget(self.num_tel_edit, 3, 1)
        layout.addWidget(self.email_label, 4, 0)
        layout.addWidget(self.email_edit, 4, 1)
        layout.addWidget(self.id_concert_label, 5, 0)
        layout.addWidget(self.id_concert_edit, 5, 1)
        layout.addWidget(self.nb_place_achete_label, 6, 0)
        layout.addWidget(self.nb_place_achete_edit, 6, 1)
        layout.addWidget(self.emplacement_label, 7, 0)
        layout.addWidget(self.emplacement_edit, 7, 1)
        layout.addWidget(self.tarif_label, 8, 0)
        layout.addWidget(self.tarif_edit, 8, 1)
        layout.addWidget(self.update_button, 9, 0, 1, 2)

        self.setLayout(layout)

    def update_user(self):
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        num_tel = self.num_tel_edit.text()
        email = self.email_edit.text()
        id_concert = self.id_concert_edit.text()
        nb_place_achete = self.nb_place_achete_edit.text()
        emplacement = self.emplacement_edit.text()
        tarif = self.tarif_edit.text()

        # Connexion à la base de données
        connection = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='admin',
            database='salle_concert'
        )
        cursor = connection.cursor()

        # Mettre à jour les données de l'utilisateur dans la base de données
        cursor.execute("UPDATE spectateurs SET nom = %s, prenom = %s, num_tel = %s, email = %s, id_concert = %s, nb_place_achete = %s, emplacement = %s, tarif = %s WHERE id = %s",
                       (nom, prenom, num_tel, email, id_concert, nb_place_achete, emplacement, tarif, self.user_id))

        connection.commit()
        connection.close()

        QMessageBox.information(self, 'Modification du compte', 'Compte modifié avec succès!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    user_id_to_modify = 13  # Remplacez ceci par l'ID de l'utilisateur que vous souhaitez modifier
    modification_app = modification_spec_bdd(user_id_to_modify)
    modification_app.show()
    sys.exit(app.exec_())
