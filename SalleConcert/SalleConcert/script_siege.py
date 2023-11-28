import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class SeatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Cinéma')
        self.setGeometry(100, 100, 400, 400)

        grid_layout = QGridLayout()
        self.setLayout(grid_layout)

        for i in range(5):
            for j in range(5):
                seat_btn = QPushButton(f"{chr(65 + i)}-{j + 1}")
                pixmap = QPixmap('../images/siege.png')
                pixmap = pixmap.scaledToWidth(50)
                icon = QIcon(pixmap)
                seat_btn.setIcon(icon)
                seat_btn.setIconSize(pixmap.size())
                grid_layout.addWidget(seat_btn, i, j)

        self.show()


def main():
    app = QApplication(sys.argv)
    seat_window = SeatWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()