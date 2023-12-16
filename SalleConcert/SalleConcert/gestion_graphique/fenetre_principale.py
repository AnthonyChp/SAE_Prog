"""
.. module:: fenetre_principale
   :platform: Unix, windows
   :synopsis: fenetre principale qui réunit les différents bout de code pour former l'application

.. moduleauthor:: Bauwens Matthieu <matthieu.bauwens@etu.univ-poitiers.fr>


"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QVBoxLayout, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, QToolBar, QAction
from PyQt5.QtGui import QIcon

from modif_spectateurs import ModifSpectateurs
from modif_concerts import ModifConcerts
from recup_spectateurs import DataSpectateurs
from recup_concerts import DataConcerts
from ajout_spectateurs import AjoutSpectateurs
from ajout_concerts import AjoutConcerts


class AppGestion(QMainWindow):

    """
    La classe AppGestion représente la fenêtre principale de l'application.

    Cette fenêtre contient deux onglets, un pour la table des spectateurs et un pour la table des concerts.
    Chaque onglet comprend une table affichant les données de la table respective, ainsi que des boutons pour rafraîchir,
    ajouter, modifier et supprimer des entrées.

    :ivar donnees_spectateurs: L'objet gérant l'accès à la base de données des spectateurs.
    :vartype donnees_spectateurs: DataSpectateurs
    :ivar donnees_concerts: L'objet gérant l'accès à la base de données des concerts.
    :vartype donnees_concerts: DataConcerts
    """

    def __init__(self, donnees_spectateurs , donnees_concerts):

        """
        Initialise une nouvelle instance de la classe AppGestion.

        :param donnees_spectateurs: L'objet gérant l'accès à la base de données des spectateurs.
        :type donnees_spectateurs: DataSpectateurs
        :param donnees_concerts: L'objet gérant l'accès à la base de données des concerts.
        :type donnees_concerts: DataConcerts
        """

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


        # Ajout de barre d'outils avec racourcis

        self.toolbar_spectateurs = QToolBar(self)
        self.addToolBar(self.toolbar_spectateurs)

        # rafraichir
        self.action_refreshs = QAction(QIcon.fromTheme('view-refresh'), 'Rafraîchir', self)

        self.action_refreshs.triggered.connect(self.refresh_donnees_spectateurs)
        self.toolbar_spectateurs.addAction(self.action_refreshs)

        # ajouter
        self.action_ajouts = QAction(QIcon.fromTheme('list-add'), 'Ajouter', self)
        self.action_ajouts.triggered.connect(self.ajout_spectateurs)
        self.toolbar_spectateurs.addAction(self.action_ajouts)

        # modifier
        self.action_modifs = QAction(QIcon.fromTheme('document-edit'), 'Modifier', self)
        self.action_modifs.triggered.connect(self.modif_donnees_spectateurs)
        self.toolbar_spectateurs.addAction(self.action_modifs)

        # supprimer
        self.action_supps = QAction(QIcon.fromTheme('edit-delete'), 'Supprimer', self)
        self.action_supps.triggered.connect(self.supp_spectateurs)
        self.toolbar_spectateurs.addAction(self.action_supps)

        self.onglet1_layout.addWidget(self.toolbar_spectateurs)



        self.table_spectateurs = QTableWidget()
        self.onglet1_layout.addWidget(self.table_spectateurs)
            # boutons
        self.bouton_refresh_spectateurs = QPushButton("Rafraîchir")
        self.bouton_refresh_spectateurs.setStyleSheet('background-color: #3498db; color: #000000;')
        self.bouton_ajout_spectateurs = QPushButton("Ajouter un spectateur")
        self.bouton_ajout_spectateurs.setStyleSheet('background-color: #009919; color: #000000;')
        self.bouton_modif_spectateurs = QPushButton("Modifier la ligne")
        self.bouton_modif_spectateurs.setStyleSheet('background-color: #ff8b00; color: #000000;')
        self.bouton_supp_spectateurs = QPushButton("Supprimer la ligne")
        self.bouton_supp_spectateurs.setStyleSheet('background-color: #fc0d0d; color: #000000;')
        self.onglet1_layout.addWidget(self.bouton_refresh_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_ajout_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_modif_spectateurs)
        self.onglet1_layout.addWidget(self.bouton_supp_spectateurs)


        # Ajouter le deuxième onglet
        self.onglet2 = QWidget()
        self.onglets.addTab(self.onglet2, "Table Concerts")
        self.onglet2_layout = QVBoxLayout(self.onglet2)

        # Ajout de barre d'outils avec racourcis

        self.toolbar_concerts = QToolBar(self)
        self.addToolBar(self.toolbar_concerts)

        # rafraîchir
        self.action_refreshc = QAction(QIcon.fromTheme('view-refresh'), 'Rafraîchir', self)
        self.action_refreshc.triggered.connect(self.refresh_donnees_concerts)
        self.toolbar_concerts.addAction(self.action_refreshc)

        # ajouter
        self.action_ajoutc = QAction(QIcon.fromTheme('list-add'), 'Ajouter', self)
        self.action_ajoutc.triggered.connect(self.ajout_concerts)
        self.toolbar_concerts.addAction(self.action_ajoutc)

        # modifier
        self.action_modifc = QAction(QIcon.fromTheme('document-edit'), 'Modifier', self)
        self.action_modifc.triggered.connect(self.modif_donnees_concerts)
        self.toolbar_concerts.addAction(self.action_modifc)

        # supprimer
        self.action_suppc = QAction(QIcon.fromTheme('edit-delete'), 'Supprimer', self)
        self.action_suppc.triggered.connect(self.supp_concerts)
        self.toolbar_concerts.addAction(self.action_suppc)

        self.onglet2_layout.addWidget(self.toolbar_concerts)



        self.table_concerts = QTableWidget()
        self.onglet2_layout.addWidget(self.table_concerts)

            # boutons
        self.bouton_refresh_concerts = QPushButton("Rafraîchir")
        self.bouton_refresh_concerts.setStyleSheet('background-color: #3498db; color: #000000;')
        self.bouton_ajout_concerts = QPushButton("Ajouter un concert")
        self.bouton_ajout_concerts.setStyleSheet('background-color: #009919; color: #000000;')
        self.bouton_modif_concerts = QPushButton("Modifier la ligne")
        self.bouton_modif_concerts.setStyleSheet('background-color: #ff8b00; color: #000000;')
        self.bouton_supp_concerts = QPushButton("Supprimer la ligne")
        self.bouton_supp_concerts.setStyleSheet('background-color: #fc0d0d; color: #000000;')


        self.onglet2_layout.addWidget(self.bouton_refresh_concerts)
        self.onglet2_layout.addWidget(self.bouton_ajout_concerts)
        self.onglet2_layout.addWidget(self.bouton_modif_concerts)
        self.onglet2_layout.addWidget(self.bouton_supp_concerts)


        self.bouton_refresh_spectateurs.clicked.connect(self.refresh_donnees_spectateurs)
        self.bouton_ajout_spectateurs.clicked.connect(self.ajout_spectateurs)
        self.bouton_modif_spectateurs.clicked.connect(self.modif_donnees_spectateurs)
        self.bouton_supp_spectateurs.clicked.connect(self.supp_spectateurs)


        self.bouton_refresh_concerts.clicked.connect(self.refresh_donnees_concerts)
        self.bouton_ajout_concerts.clicked.connect(self.ajout_concerts)
        self.bouton_modif_concerts.clicked.connect(self.modif_donnees_concerts)
        self.bouton_supp_concerts.clicked.connect(self.supp_concerts)


        self.refresh_donnees_spectateurs()
        self.refresh_donnees_concerts()


    def refresh_donnees_spectateurs(self):
        
        """
        Rafraîchit la table des spectateurs en récupérant les données de la base de données.
        """

        query = "SELECT * FROM spectateurs"
        data = self.donnees_spectateurs.recup_donnees_spectateurs(query)

        self.table_spectateurs.setRowCount(0)
        self.table_spectateurs.setColumnCount(len(data[0]))
        self.table_spectateurs.setHorizontalHeaderLabels([str(header[0]) for header in self.donnees_spectateurs.cursor.description])

        for row_number, row_data in enumerate(data):
            self.table_spectateurs.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_spectateurs.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))


    def ajout_spectateurs(self):

        """
        Ouvre une boîte de dialogue pour ajouter un nouveau spectateur à la base de données.
        """

        AjoutSpectateurs(self.donnees_spectateurs).exec_()

        self.refresh_donnees_spectateurs()


    def modif_donnees_spectateurs(self):

        """
        Ouvre une boîte de dialogue pour modifier les données d'un spectateur sélectionné dans la table.
        """

        selected_row = self.table_spectateurs.currentRow()
        if selected_row != -1:
            data_to_edit = [self.table_spectateurs.item(selected_row, col).text() for col in range(self.table_spectateurs.columnCount())]
            ModifSpectateurs(data_to_edit, self.donnees_spectateurs).exec_()
            self.refresh_donnees_spectateurs()

    def supp_spectateurs(self):

        """
        Supprime un spectateur sélectionné dans la table après confirmation de l'utilisateur.
        """
        
        selected_row = self.table_spectateurs.currentRow()
        if selected_row != -1:
            confirmation = QMessageBox.question(self, 'Suppression', 'Êtes-vous sûr de vouloir supprimer cette ligne ?', 
                                               QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:

                                # Récupérer l'ID de la ligne sélectionnée
                id_a_supprimer = self.table_spectateurs.item(selected_row, 0).text()

                # Construire la requête DELETE
                delete_query = "DELETE FROM spectateurs WHERE ID = %s"

                self.donnees_spectateurs.execute_spectateurs_query(delete_query, (id_a_supprimer,))


                self.table_spectateurs.removeRow(selected_row)



    def refresh_donnees_concerts(self):

        """
        Rafraîchit la table des concerts en récupérant les données de la base de données.
        """

        query = "SELECT * FROM concerts"
        data = self.donnees_concerts.recup_donnees_concerts(query)

        self.table_concerts.setRowCount(0)
        self.table_concerts.setColumnCount(len(data[0]))
        self.table_concerts.setHorizontalHeaderLabels([str(header[0]) for header in self.donnees_concerts.cursor.description])

        for row_number, row_data in enumerate(data):
            self.table_concerts.insertRow(row_number)
            for column_number, column_data in enumerate(row_data):
                self.table_concerts.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

    def ajout_concerts(self):

        """
        Ouvre une boîte de dialogue pour ajouter un nouveau concert à la base de données.
        """

        AjoutConcerts(self.donnees_concerts).exec_()

        self.refresh_donnees_concerts()


    def modif_donnees_concerts(self):

        """
        Ouvre une boîte de dialogue pour modifier les données d'un concert sélectionné dans la table.
        """

        selected_row = self.table_concerts.currentRow()
        if selected_row != -1:
            data_to_edit = [self.table_concerts.item(selected_row, col).text() for col in range(self.table_concerts.columnCount())]
            ModifConcerts(data_to_edit, self.donnees_concerts).exec_()
            self.refresh_donnees_concerts()

    def supp_concerts(self):

        """
        Supprime un concert sélectionné dans la table après confirmation de l'utilisateur.
        """
        
        selected_row = self.table_concerts.currentRow()
        if selected_row != -1:
            confirmation = QMessageBox.question(self, 'Suppression', 'Êtes-vous sûr de vouloir supprimer cette ligne ?', 
                                               QMessageBox.Yes | QMessageBox.No)

            if confirmation == QMessageBox.Yes:

                                # Récupérer l'ID de la ligne sélectionnée
                id_a_supprimer = self.table_concerts.item(selected_row, 0).text()

                # Construire la requête DELETE
                delete_query = "DELETE FROM concerts WHERE ID = %s"

                self.donnees_concerts.execute_concerts_query(delete_query, (id_a_supprimer,))

                self.table_concerts.removeRow(selected_row)


