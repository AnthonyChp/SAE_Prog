from PyQt5.QtWidgets import QWidget
import mysql.connector

class DataConcerts(QWidget):
    def __init__(self):
        super().__init__()
        self.connexion_bdd = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="salle_concert"
        )
        self.cursor = self.connexion_bdd.cursor()

    def recup_donnees_concerts(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_concerts_query(self, query, data):
        self.cursor.execute(query, data)
        self.connexion_bdd.commit()
