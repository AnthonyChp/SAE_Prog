from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QVBoxLayout, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem

from modif_spectateurs import ModifSpectateurs
from modif_concerts import ModifConcerts
from recup_spectateurs import DataSpectateurs
from recup_concerts import DataConcerts

class AppGestion(QMainWindow):
    def __init__(self, donnees_spectateurs , donnees_concerts):
        super().__init__()
        self.donnees_spectateurs = donnees_spectateurs
        self.donnees_concerts = donnees_concerts

        self.setWindowTitle('Gestion graphique de la base de données salle_concert')
        self.resize(800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.onglets = QTabWidget(self)
        self.layout.addWidget(self.onglets)

        self.onglet1 = QWidget()
        self.onglets.addTab(self.onglet1, "Table Spectateurs")
        self.onglet1_layout = QVBoxLayout(self.onglet1)
        self.table_spectateurs = QTableWidget()
        self.onglet1_layout.addWidget(self.table_spectateurs)
        self.bouton_refresh_spectateurs = QPushButton("Rafraîchir")
        self.bouton_ajout_spectateurs = QPushButton("Ajouter une ligne")
        self.bouton_modif_spectateurs = QPushButton("Modifier la ligne")
        self.bouton_supp_spectateurs = QPushButton("Supprimer la ligne")
        self.onglet1_layout.addWidget(self.bouton_refresh_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_ajout_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_modif_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_supp_spectateurs)


        # Ajouter le deuxième onglet
        self.onglet2 = QWidget()
        self.onglets.addTab(self.onglet2, "Table Concerts")
        self.onglet2_layout = QVBoxLayout(self.onglet2)
        self.table_concerts = QTableWidget()
        self.onglet2_layout.addWidget(self.table_concerts)
        self.bouton_refresh_concerts = QPushButton("Rafraîchir")
        self.bouton_ajout_concerts = QPushButton("Ajouter une ligne")
        self.bouton_modif_concerts = QPushButton("Modifier la ligne")
        self.bouton_supp_concerts = QPushButton("Supprimer la ligne")
        self.onglet2_layout.addWidget(self.bouton_refresh_concerts)
        self.onglet2_layout.addWidget(self.bouton_ajout_concerts)
        self.onglet2_layout.addWidget(self.bouton_modif_concerts)
        self.onglet2_layout.addWidget(self.bouton_supp_concerts)


        self.bouton_refresh_spectateurs.clicked.connect(self.refresh_donnees_spectateurs)
        self.bouton_ajout_spectateurs.clicked.connect(self.ajout_donnees_spectateurs)
        self.bouton_modif_spectateurs.clicked.connect(self.modif_donnees_spectateurs)
        self.bouton_supp_spectateurs.clicked.connect(self.supp_spectateurs)


        self.bouton_refresh_concerts.clicked.connect(self.refresh_donnees_concerts)
        self.bouton_ajout_concerts.clicked.connect(self.ajout_donnees_concerts)
        self.bouton_modif_concerts.clicked.connect(self.modif_donnees_concerts)
        self.bouton_supp_concerts.clicked.connect(self.supp_concerts)


        self.refresh_donnees_spectateurs()
        self.refresh_donnees_concerts()


    def refresh_donnees_spectateurs(self):
        # Fetch data from the database
        query = "SELECT * FROM spectateurs"
        data = self.donnees_spectateurs.recup_donnees_spectateurs(query)

        # Populate the table with the fetched data
        self.table_spectateurs.setRowCount(0)
        self.table_spectateurs.setColumnCount(len(data[0]))
        self.table_spectateurs.setHorizontalHeaderLabels([str(header[0]) for header in self.donnees_spectateurs.cursor.description])

        for row_number, row_data in enumerate(data):
            self.table_spectateurs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_spectateurs.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))


    def ajout_donnees_spectateurs(self):

        pass

    def modif_donnees_spectateurs(self):
        selected_row = self.table_spectateurs.currentRow()
        if selected_row != -1:
            data_to_edit = [self.table_spectateurs.item(selected_row, col).text() for col in range(self.table_spectateurs.columnCount())]

            edit_dialog = ModifSpectateurs(data_to_edit, self.donnees_spectateurs)
            if edit_dialog.exec_():
                edited_data = edit_dialog.get_edited_data()

                # Update the database with the edited data
                update_query = "UPDATE spectateurs SET nom = %s, prenom = %s, num_tel = %s, email = %s, mot_de_passe = %s, id_concert = %s, nb_place_achete = %s, emplacement = %s, tarif = %s WHERE ID = %s"
                self.donnees_spectateurs.execute_spectateurs_query(update_query, edited_data[1:] + [edited_data[0]])

                # Refresh the data in the table
                self.refresh_donnees_spectateurs()

    def supp_spectateurs(self):
        selected_row = self.table_spectateurs.currentRow()
        if selected_row != -1:
            confirmation = QMessageBox.question(self, 'Suppression', 'Êtes-vous sûr de vouloir supprimer cette ligne ?', 
                                               QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                # Supprimer la ligne sélectionnée
                

                                # Récupérer l'ID de la ligne sélectionnée
                id_a_supprimer = self.table_spectateurs.item(selected_row, 0).text()

                # Construire la requête DELETE
                delete_query = "DELETE FROM spectateurs WHERE ID = %s"

                self.donnees_spectateurs.execute_spectateurs_query(delete_query, (id_a_supprimer,))
                #self.connexion_bdd.commit()

                self.table_spectateurs.removeRow(selected_row)



    def refresh_donnees_concerts(self):
        # Fetch data from the database
        query = "SELECT * FROM concerts"
        data = self.donnees_concerts.recup_donnees_concerts(query)

        # Populate the table with the fetched data
        self.table_concerts.setRowCount(0)
        self.table_concerts.setColumnCount(len(data[0]))
        self.table_concerts.setHorizontalHeaderLabels([str(header[0]) for header in self.donnees_concerts.cursor.description])

        for row_number, row_data in enumerate(data):
            self.table_concerts.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_concerts.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

    def ajout_donnees_concerts(self):

        pass


    def modif_donnees_concerts(self):
        selected_row = self.table_concerts.currentRow()
        if selected_row != -1:
            data_to_edit = [self.table_concerts.item(selected_row, col).text() for col in range(self.table_concerts.columnCount())]

            edit_dialog = ModifConcerts(data_to_edit, self.donnees_concerts)
            if edit_dialog.exec_():
                edited_data = edit_dialog.get_edited_data()

                # Update the database with the edited data
                update_query = "UPDATE concerts SET titre = %s, artiste = %s, date = %s, tarif = %s WHERE ID = %s"
                self.donnees_concerts.execute_concerts_query(update_query, edited_data[1:] + [edited_data[0]])

                # Refresh the data in the table
                self.refresh_donnees_concerts()

    def supp_concerts(self):
        selected_row = self.table_concerts.currentRow()
        if selected_row != -1:
            confirmation = QMessageBox.question(self, 'Suppression', 'Êtes-vous sûr de vouloir supprimer cette ligne ?', 
                                               QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:
                # Supprimer la ligne sélectionnée
                

                                # Récupérer l'ID de la ligne sélectionnée
                id_a_supprimer = self.table_concerts.item(selected_row, 0).text()

                # Construire la requête DELETE
                delete_query = "DELETE FROM concerts WHERE ID = %s"

                self.donnees_concerts.execute_concerts_query(delete_query, (id_a_supprimer,))
                #self.connexion_bdd.commit()

                self.table_concerts.removeRow(selected_row)


