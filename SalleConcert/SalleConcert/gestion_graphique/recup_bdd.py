import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QGridLayout, QLabel, QLineEdit
import mysql.connector


class RecupBDD(QWidget):

    def __init__(self):
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="salle_concert"
        )
        self.cursor = self.db_connection.cursor()

    def fetch_data(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_query(self, query, data):
        self.cursor.execute(query, data)
        self.db_connection.commit()
