import sys
from PyQt5.QtWidgets import QApplication

from fenetre_principale import AppGestion
from recup_spectateurs import DataSpectateurs
from recup_concerts import DataConcerts

def main():
    application = QApplication(sys.argv)
    donnees_spectateurs = DataSpectateurs()
    donnees_concerts = DataConcerts()
    fenetre_principale = AppGestion(donnees_spectateurs, donnees_concerts)
    fenetre_principale.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()