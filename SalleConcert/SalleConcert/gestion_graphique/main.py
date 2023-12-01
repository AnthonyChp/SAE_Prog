import sys
from PyQt5.QtWidgets import QApplication

from fenetre_principale import AppGestion
from recup_bdd import RecupBDD


def main():
    app = QApplication(sys.argv)
    data_manager = RecupBDD()
    window = AppGestion(data_manager)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
