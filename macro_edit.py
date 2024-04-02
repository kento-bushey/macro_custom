import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import csv

class RECORD:
    def __init__(self):
        self.history = []
        self.history_key = []

    def print(self):
        print(self.history_key)
        print(self.history)

    def import_csv(self, filename):
        print("Importing...")
        history_dict = {}
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            for row in reader:
                char = row[0]
                pairs = []
                pair_strings = row[1:]
                for pair_str in pair_strings:
                    pair = eval(pair_str)
                    pairs.append(pair)
                history_dict[char] = pairs
                self.history_key.append(char)
        for i in range(len(self.history_key)):
            self.history.append(history_dict[self.history_key[i]])
        self.print()

    def convert_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Character', 'Press-Release Pairs'])
            for char, times in self.history.items():
                row = [char]
                for press_time, release_time in times:
                    row.append((press_time, release_time))
                writer.writerow(row)
    


class Canvas(QtWidgets.QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1000, 400)
        self.setStyleSheet("background-color: grey;")

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x = event.x()
            y = event.y()
            print(f"Clicked at ({x}, {y})")

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macro Edit")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.resize(800, 500)
        
        self.record = RECORD()  # Create an instance of RECORD class
        
        # File Menu
        file_menu = QtWidgets.QMenuBar()
        file_menu_action = file_menu.addMenu("File")
        open_action = QtWidgets.QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu_action.addAction(open_action)
        layout.setMenuBar(file_menu)
        
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
        
    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        if filename:
            self.record.import_csv(filename)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())