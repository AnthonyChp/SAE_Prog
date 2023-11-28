from PyQt5.QtWidgets import QPushButton

class SeatButton(QPushButton):
    def __init__(self, row, col, concert_name):
        super().__init__(concert_name)
        self.row = row
        self.col = col
