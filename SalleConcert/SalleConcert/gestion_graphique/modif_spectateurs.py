"""
.. module:: modif_spectateurs
   :platform: Unix, windows
   :synopsis: classe pour assurer la modification des spectateurs dans la base de données

.. moduleauthor:: Bauwens Matthieu <matthieu.bauwens@etu.univ-poitiers.fr>


"""

from PyQt5.QtWidgets import QLabel, QDialog, QPushButton, QLineEdit, QMessageBox, QGridLayout
import bcrypt

class ModifSpectateurs(QDialog):

    """
    classe ModifSpectateurs qui permet de modifier des spectateurs dans la base de données

    :param data_to_edit: les données du spectateur à éditer.
    :type data_to_edit: tuple
    :param donnees_spectateurs: l'objet gérant l'accès à la base de données des spectateurs.
    :type donnees_spectateurs: DatabaseManager
    
    """
        
    def __init__(self, data_to_edit, donnees_spectateurs):

        """
        initialise une nouvelle instance de la classe ModifSpectateurs.

        :param data_to_edit: les données du spectateur à éditer.
        :type data_to_edit: tuple
        :param donnees_spectateurs: l'objet gérant l'accès à la base de données des spectateurs.
        :type donnees_spectateurs: DatabaseManager
        """
        
        super().__init__()
        self.donnees_spectateurs = donnees_spectateurs
        self.data_to_edit = data_to_edit

        self.setWindowTitle('Modification de spectateur')
        self.resize(500, 350)

        self.nom_label = QLabel('Nom :')
        self.nom_edit = QLineEdit(data_to_edit[1])

        self.prenom_label = QLabel('Prénom :')
        self.prenom_edit = QLineEdit(data_to_edit[2])

        self.num_tel_label = QLabel('Numéro de téléphone :')
        self.num_tel_edit = QLineEdit(data_to_edit[3])

        self.email_label = QLabel('Adresse e-mail :')
        self.email_edit = QLineEdit(data_to_edit[4])

        self.password_label = QLabel('Mot de passe :')
        self.password_edit = QLineEdit(data_to_edit[5])
        self.password_edit.setEchoMode(QLineEdit.Password)  # Masquer le mot de passe

        self.id_concert_label = QLabel('ID du Concert :')
        self.id_concert_edit = QLineEdit(data_to_edit[6])

        self.nb_place_achete_label = QLabel('Nombre de places achetées :')
        self.nb_place_achete_edit = QLineEdit(data_to_edit[7])

        self.emplacement_label = QLabel('Emplacement :')
        self.emplacement_edit = QLineEdit(data_to_edit[8])

        self.tarif_label = QLabel('Tarif :')
        self.tarif_edit = QLineEdit(data_to_edit[9])

        layout = QGridLayout()

        self.bouton_modif = QPushButton("Confirmer la modification")
        layout.addWidget(self.bouton_modif)

        # Connecter le bouton à la fonction
        self.bouton_modif.clicked.connect(self.modifier_spectateurs)

        layout.addWidget(self.nom_label, 0, 0)
        layout.addWidget(self.nom_edit, 0, 1)
        layout.addWidget(self.prenom_label, 1, 0)
        layout.addWidget(self.prenom_edit, 1, 1)
        layout.addWidget(self.num_tel_label, 2, 0)
        layout.addWidget(self.num_tel_edit, 2, 1)
        layout.addWidget(self.email_label, 3, 0)
        layout.addWidget(self.email_edit, 3, 1)
        layout.addWidget(self.password_label,4, 0)
        layout.addWidget(self.password_edit, 4, 1)
        layout.addWidget(self.id_concert_label, 5, 0)
        layout.addWidget(self.id_concert_edit, 5, 1)
        layout.addWidget(self.nb_place_achete_label, 6, 0)
        layout.addWidget(self.nb_place_achete_edit, 6, 1)
        layout.addWidget(self.emplacement_label, 7, 0)
        layout.addWidget(self.emplacement_edit, 7, 1)
        layout.addWidget(self.tarif_label, 8, 0)
        layout.addWidget(self.tarif_edit, 8, 1)
        layout.addWidget(self.bouton_modif, 9, 0, 1, 2)

        self.setLayout(layout)

    def modifier_spectateurs(self):

        """
        Fonction appelée lorsqu'on clique sur le bouton de modification.

        Elle récupère les valeurs des champs de saisie, valide les champs, effectue le hachage du mot de passe,
        construit la requête UPDATE puis exécute la requête.
        """

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

        # Construire la requête UPDATE
        query_modif = "UPDATE spectateurs SET nom = %s, prenom = %s, num_tel = %s, email = %s, mot_de_passe = %s, id_concert = %s, nb_place_achete = %s, emplacement = %s, tarif = %s WHERE ID = %s"
        valeurs = (nom, prenom, num_tel, email, hashed_password, id_concert or None, nb_place_achete or None, emplacement or None, tarif or None, self.data_to_edit[0])
        # Exécuter la requête UPDATE dans la base de données
        self.donnees_spectateurs.execute_spectateurs_query(query_modif, valeurs)

        self.accept()
