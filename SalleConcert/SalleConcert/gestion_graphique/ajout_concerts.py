from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QPushButton, QLineEdit, QMessageBox


class AjoutConcerts(QDialog):
    def __init__(self, donnees_concerts):
        super().__init__()
        self.donnees_concerts = donnees_concerts

        self.setWindowTitle('Ajout de concert')
        self.resize(300, 200)

        self.layout = QVBoxLayout(self)

        # Display labels and line edits for each column
        self.line_edits = []
        for label in ["Titre", "Artiste", "Date", "Tarif"]:
            label_widget = QLabel(label)
            line_edit = QLineEdit()

            self.layout.addWidget(label_widget)
            self.layout.addWidget(line_edit)

            self.line_edits.append(line_edit)

        # Button to confirm the addition
        self.confirm_button = QPushButton("Confirmer l'ajout")
        self.layout.addWidget(self.confirm_button)

        # Connect the button to the function
        self.confirm_button.clicked.connect(self.ajouter_concert)

    def ajouter_concert(self):
        # Récupérer les valeurs des champs de saisie
        titre = self.line_edits[0].text()
        artiste = self.line_edits[1].text()
        date = self.line_edits[2].text()
        tarif = self.line_edits[3].text()

        # Valider que tous les champs sont remplis
        if not titre or not artiste or not date or not tarif:
            QMessageBox.warning(self, 'Champs non remplis', 'Veuillez remplir tous les champs.')
            return

        # Construire la requête INSERT
        query_ajout = "INSERT INTO concerts (titre, artiste, date, tarif) VALUES (%s, %s, %s, %s)"
        valeurs = (titre, artiste, date, tarif ) # Remplacez les points de suspension par d'autres valeurs

   
        # Exécuter la requête INSERT dans la base de données
        self.donnees_concerts.execute_concerts_query(query_ajout, valeurs)


        self.accept()

