"""
.. module:: ajout_concerts
   :platform: Unix, windows
   :synopsis: classe pour ajouter des concerts dans la base de données

.. moduleauthor:: Bauwens Matthieu <matthieu.bauwens@etu.univ-poitiers.fr>


"""

from PyQt5.QtWidgets import QLabel, QDialog, QGridLayout, QPushButton, QLineEdit, QMessageBox, QDateEdit

class AjoutConcerts(QDialog):

    """
    classe AjoutConcerts qui permet d'ajouter des concerts dans la base de données.

    :param donnees_concerts: l'objet gérant l'accès à la base de données des concerts.
    :type donnees_concerts: DatabaseManager
    """
    
    def __init__(self, donnees_concerts):

        """
        initialise une nouvelle instance de la classe AjoutConcerts.

        :param donnees_concerts: l'objet gérant l'accès à la base de données des concerts.
        :type donnees_concerts: DatabaseManager
        """

        super().__init__()

        self.donnees_concerts = donnees_concerts

        self.setWindowTitle('Ajout de concert')
        self.resize(500, 350)

        self.titre_label = QLabel('Titre :')
        self.titre_edit = QLineEdit()

        self.artiste_label = QLabel('Artiste :')
        self.artiste_edit = QLineEdit()

        self.date_label = QLabel('Date :')
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)

        self.tarif_label = QLabel('Tarif :')
        self.tarif_edit = QLineEdit()

        layout = QGridLayout()

        self.bouton_ajout = QPushButton("Confirmer l'ajout")
        layout.addWidget(self.bouton_ajout)

        # Connect the button to the function
        self.bouton_ajout.clicked.connect(self.ajouter_concert)

    
        layout.addWidget(self.titre_label, 0, 0)
        layout.addWidget(self.titre_edit, 0, 1)
        layout.addWidget(self.artiste_label, 1, 0)
        layout.addWidget(self.artiste_edit, 1, 1)
        layout.addWidget(self.date_label, 2, 0)
        layout.addWidget(self.date_edit, 2, 1)
        layout.addWidget(self.tarif_label, 3, 0)
        layout.addWidget(self.tarif_edit, 3, 1)
        layout.addWidget(self.bouton_ajout, 4, 0, 1, 2)

        self.setLayout(layout)


    def ajouter_concert(self):

        """
        Fonction appelée lorsqu'on clique sur le bouton d'ajout de concert.

        Récupère les valeurs des champs de saisie, valide les champs, construit la requête SQL d'insertion,
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

        date_bon = date.toPyDate().isoformat()

        # Construire la requête INSERT
        query_ajout = "INSERT INTO concerts (titre, artiste, date, tarif) VALUES (%s, %s, %s, %s)"
        valeurs = (titre, artiste, date_bon, tarif) # Remplacez les points de suspension par d'autres valeurs

   
        # Exécuter la requête INSERT dans la base de données
        self.donnees_concerts.execute_concerts_query(query_ajout, valeurs)


        self.accept()