from PyQt5.QtWidgets import QLabel, QDialog, QGridLayout, QPushButton, QLineEdit, QMessageBox
import bcrypt

class AjoutSpectateurs(QDialog):
    def __init__(self, donnees_spectateurs):
        super().__init__()

        self.donnees_spectateurs = donnees_spectateurs

        self.setWindowTitle('Ajout de spectateur')
        self.resize(500, 350)

        self.nom_label = QLabel('Nom :')
        self.nom_edit = QLineEdit() 

        self.prenom_label = QLabel('Prénom :')
        self.prenom_edit = QLineEdit() 

        self.num_tel_label = QLabel('Numéro de téléphone :')
        self.num_tel_edit = QLineEdit()  

        self.email_label = QLabel('Adresse e-mail :')
        self.email_edit = QLineEdit() 

        self.password_label = QLabel('Mot de passe :')
        self.password_edit = QLineEdit()

        self.id_concert_label = QLabel('ID du Concert :')
        self.id_concert_edit = QLineEdit()

        self.nb_place_achete_label = QLabel('Nombre de places achetées :')
        self.nb_place_achete_edit = QLineEdit()

        self.emplacement_label = QLabel('Emplacement :')
        self.emplacement_edit = QLineEdit()

        self.tarif_label = QLabel('Tarif :')
        self.tarif_edit = QLineEdit()


        layout = QGridLayout()

        self.bouton_ajout = QPushButton("Confirmer l'ajout")
        layout.addWidget(self.bouton_ajout)

        # Connect the button to the function
        self.bouton_ajout.clicked.connect(self.ajouter_spectateur)

    
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
        layout.addWidget(self.id_concert_label, 5, 0)
        layout.addWidget(self.id_concert_edit, 5, 1)
        layout.addWidget(self.nb_place_achete_label, 6, 0)
        layout.addWidget(self.nb_place_achete_edit, 6, 1)
        layout.addWidget(self.emplacement_label, 7, 0)
        layout.addWidget(self.emplacement_edit, 7, 1)
        layout.addWidget(self.tarif_label, 8, 0)
        layout.addWidget(self.tarif_edit, 8, 1)
        layout.addWidget(self.bouton_ajout, 9, 0, 1, 2)

        self.setLayout(layout)


    def ajouter_spectateur(self):
        # Récupérer les valeurs des champs de saisie
        nom = self.nom_edit.text()
        prenom = self.prenom_edit.text()
        num_tel = self.num_tel_edit.text()
        email = self.email_edit.text()
        password = self.password_edit.text()
        id_concert = self.id_concert_edit.text()
        nb_place_achete = self.nb_place_achete_edit.text()
        emplacement = self.emplacement_edit.text()
        tarif = self.tarif_edit.text()

        # Valider que tous les champs sont remplis
        if not nom or not prenom or not num_tel or not email or not password:
            QMessageBox.warning(self, 'Champs non remplis', 'Veuillez remplir tous les champs.')
            return

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Construire la requête INSERT
        query_ajout = "INSERT INTO spectateurs (nom, prenom, num_tel, email , mot_de_passe, id_concert, nb_place_achete, emplacement, tarif) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valeurs = (nom, prenom, num_tel, email, hashed_password, id_concert or None, nb_place_achete or None, emplacement or None, tarif or None) # Remplacez les points de suspension par d'autres valeurs

   
        # Exécuter la requête INSERT dans la base de données
        self.donnees_spectateurs.execute_spectateurs_query(query_ajout, valeurs)

        self.accept()