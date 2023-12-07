import sys
from PyQt5.QtWidgets import QApplication
from reservation_app import ReservationApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ReservationApp()
    sys.exit(app.exec_())