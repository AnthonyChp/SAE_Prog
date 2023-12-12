"""
.. module:: main
   :platform: Unix, Windows
   :synopsis: Lancement de l'application.

.. moduleauthor:: Chapus Anthony <anthony.chapus1002@etu.univ-poitiers.fr>

"""
import sys
from PyQt5.QtWidgets import QApplication
from reservation_app import ReservationApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReservationApp()
    sys.exit(app.exec_())