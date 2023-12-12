"""
.. module:: gestion_graphique
   :platform: Unix, windows
   :synopsis: classe pour modifier des concerts dans la base de données

.. moduleauthor:: Bauwens Matthieu <matthieu.bauwens@etu.univ-poitiers.fr>


"""

from PyQt5.QtWidgets import QLabel, QDialog, QGridLayout, QPushButton, QLineEdit, QMessageBox, QDateEdit
from PyQt5.QtCore import QDate

class ModifConcerts(QDialog):

    """
    classe ModifConcerts qui permet de modifier des concerts dans la base de données

    :param data_to_edit: les données du spectateur à éditer.
    :type data_to_edit: tuple
    :param donnees_concerts: l'objet gérant l'accès à la base de données des spectateurs.
    :type donnees_concerts: DatabaseManager
    
    """

    def __init__(self, data_to_edit, donnees_concerts):

        """
        initialise une nouvelle instance de la classe ModifConcerts.

        :param data_to_edit: les données du concert à éditer.
        :type data_to_edit: tuple
        :param donnees_concerts: l'objet gérant l'accès à la base de données des spectateurs.
        :type donnees_concerts: DatabaseManager
        """

        super().__init__()

        self.donnees_concerts = donnees_concerts
        self.data_to_edit = data_to_edit

        self.setWindowTitle('Modification de concert')
        self.resize(500, 350)

        self.titre_label = QLabel('Titre :')
        self.titre_edit = QLineEdit(data_to_edit[1]) 

        self.artiste_label = QLabel('Artiste :')
        self.artiste_edit = QLineEdit(data_to_edit[2]) 

        self.date_label = QLabel('Date :')
        self.date_edit = QDateEdit(QDate.fromString(data_to_edit[3], "yyyy-MM-dd")) #besoin de cette ligne pour afficher la date au format désiré et non au format str
        self.date_edit.setCalendarPopup(True) # ligne pour afficher un calendrier

        self.tarif_label = QLabel('Tarif :')
        self.tarif_edit = QLineEdit(data_to_edit[4]) 

        layout = QGridLayout()

        self.bouton_modif = QPushButton("Confirmer l'ajout")
        layout.addWidget(self.bouton_modif)

        # Connect the button to the function
        self.bouton_modif.clicked.connect(self.modif_concerts)

    
        layout.addWidget(self.titre_label, 0, 0)
        layout.addWidget(self.titre_edit, 0, 1)
        layout.addWidget(self.artiste_label, 1, 0)
        layout.addWidget(self.artiste_edit, 1, 1)
        layout.addWidget(self.date_label, 2, 0)
        layout.addWidget(self.date_edit, 2, 1)
        layout.addWidget(self.tarif_label, 3, 0)
        layout.addWidget(self.tarif_edit, 3, 1)
        layout.addWidget(self.bouton_modif, 4, 0, 1, 2)

        self.setLayout(layout)


    def modif_concerts(self):

        """
        Fonction appelée lorsqu'on clique sur le bouton de modification.

        Elle récupère les valeurs des champs de saisie, valide les champs, construit la requête SQL d'insertion,
        et exécute la requête dans la base de données.
        """

        titre = self.titre_edit.text()
        artiste = self.artiste_edit.text()
        date = self.date_edit.date()
        tarif = self.tarif_edit.text()

        # Valider que tous les champs sont remplis
        if not titre or not artiste or not date or not tarif:
            QMessageBox.warning(self, 'Champs non remplis', 'Veuillez remplir tous les champs.')
            return

        date_bon = date.toPyDate().isoformat() # ligne pour tran,sformer la date en format compatible avec notre champ de bdd

        # Construire la requête UPDATE
        query_modif = "UPDATE concerts SET titre = %s, artiste = %s, date = %s, tarif = %s WHERE ID = %s"
        valeurs = (titre, artiste, date_bon, tarif, self.data_to_edit[0])

   
        # Exécuter la requête INSERT dans la base de données
        self.donnees_concerts.execute_concerts_query(query_modif, valeurs)


        self.accept()