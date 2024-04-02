import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class Canvas(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 400)
        self.setStyleSheet("background-color: white;")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        painter.drawRect(QtCore.QRect(50, 50, 100, 100))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.green))
        painter.drawEllipse(QtCore.QRect(200, 50, 150, 100))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.blue))
        painter.drawPie(QtCore.QRect(400, 50, 200, 200), 0, 180 * 16)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x = event.x()
            y = event.y()
            print(f"Clicked at ({x}, {y})")

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Canvas Example")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.resize(800, 500)

        scroll_area = QtWidgets.QScrollArea()
        layout.addWidget(scroll_area)

        canvas = Canvas()
        scroll_area.setWidget(canvas)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        start_label = QtWidgets.QLabel("Start: ")
        start_label.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(start_label)

        end_label = QtWidgets.QLabel("End: ")
        end_label.setAlignment(QtCore.Qt.AlignLeft)
        layout.addWidget(end_label)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())