import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import csv

def sec2time(sec):
    minutes, seconds = divmod(sec, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:06.3f}".format(int(hours), int(minutes), seconds)

def time2sec(time_str):
    hours, minutes, seconds = map(float, time_str.split(':'))
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return float(total_seconds)

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

    def convert_to_csv(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Character', 'Press-Release Pairs'])
            for index in range(len(self.history)):
                row = [self.history_key[index]]
                times = self.history[index]
                for press_time, release_time in times:
                    row.append((press_time, release_time))
                writer.writerow(row)
    
class RECT:
    def __init__(self, row,col,x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.row = row
        self.col = col
        self.selected = False
        self.left = x
        self.right = x + self.width
        self.bottom = y + self.height
        self.top = y
    def in_bounds(self,x,y):
        if x>=self.left and x<=self.right and y<=self.bottom and y >=self.top:
            return True
        return False

class Canvas(QtWidgets.QFrame):
    clicked = QtCore.pyqtSignal(int, int)
    ybuffer = 25
    xbuffer = 50
    track_height = 50
    scale = 100

    def __init__(self):
        super().__init__()
        self.setMinimumSize(2000, 400)
        self.setStyleSheet("background-color: grey;")
        self.rect_history = []
        self.letters = []
        self.selected = []
    
    def update_history(self, history, letters):
        print("Updating history...")
        for i in range(len(history)):
            for j in range(len(history[i])):
                left = history[i][j][0]
                right = history[i][j][1]
                x = int(self.scale*left+self.xbuffer)
                y = int( (i*self.track_height))
                width = int(self.scale*(right-left))
                height = self.track_height
                self.rect_history.append(RECT(i,j,x,y,width,height))
        self.letters = letters

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            x = event.x()
            y = event.y()

            for rect in self.rect_history:
                if rect.in_bounds(x,y):
                    for selected_rect in self.selected:
                        selected_rect.selected = False
                    selected_rect = []
                    rect.selected = True
                    self.selected.append(rect)
                    self.clicked.emit(rect.row, rect.col)

    def draw_background(self, painter):
        for i in range(10):
            brush = QtGui.QBrush(QtGui.QColor("dark grey"))  # Set the color to blue
            painter.setBrush(brush)
            painter.setPen(QtCore.Qt.NoPen)  # Set the pen to be transparent
            painter.drawRect(0, (2*i)*self.track_height, 10000, self.track_height)

    def draw_letter_tracks(self, painter):
        for i in range(len(self.letters)):
            brush = QtGui.QBrush(QtGui.QColor("light blue")) 
            painter.setBrush(brush)
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
            painter.drawRect(0,i*self.track_height,self.xbuffer,self.track_height)

            text = self.letters[i]
            text_rect = QtCore.QRect(0, i * self.track_height, self.xbuffer, self.track_height)
            painter.drawText(text_rect, QtCore.Qt.AlignCenter, text)

    def paintEvent(self,event):
        painter = QtGui.QPainter(self)
        self.draw_background(painter)
        self.draw_letter_tracks(painter)
        for rect in self.rect_history:
            brush = QtGui.QBrush(QtGui.QColor("blue")) 
            painter.setPen(QtGui.QPen(QtCore.Qt.black))
            if rect.selected:
                painter.setPen(QtGui.QPen(QtCore.Qt.white))
            painter.setBrush(brush)
            painter.drawRect(rect.x,rect.y,rect.width,rect.height)

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macro Edit")
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)
        self.resize(800, 500)

        self.curr_key = (0,0)
        self.curr_row = -1
        self.curr_col = -1
        
        #record management
        self.record = RECORD()  # Create an instance of RECORD class
        
        # File Menu
        file_menu = QtWidgets.QMenuBar()
        file_menu_action = file_menu.addMenu("File")
        open_action = QtWidgets.QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu_action.addAction(open_action)

        save_action = QtWidgets.QAction("Save", self)
        save_action.triggered.connect(self.save_file_dialog)
        file_menu_action.addAction(save_action)
        layout.setMenuBar(file_menu)
        
        scroll_area = QtWidgets.QScrollArea()
        layout.addWidget(scroll_area)

        self.canvas = Canvas()
        scroll_area.setWidget(self.canvas)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        # Start label and input box
        start_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(start_layout)

        start_label = QtWidgets.QLabel("Start: ")
        start_label.setAlignment(QtCore.Qt.AlignLeft)
        start_layout.addWidget(start_label)

        self.start_input = QtWidgets.QLineEdit()
        self.start_input.setMaximumWidth(100)  # Adjust width here
        self.start_input.setText("00:00.000")  # Set default text here
        start_layout.addWidget(self.start_input)

        start_button = QtWidgets.QPushButton("Apply")
        start_button.clicked.connect(self.apply_start)
        start_layout.addWidget(start_button)

        # End label and input box
        end_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(end_layout)

        end_label = QtWidgets.QLabel("End: ")
        end_label.setAlignment(QtCore.Qt.AlignLeft)
        end_layout.addWidget(end_label)

        self.end_input = QtWidgets.QLineEdit()
        self.end_input.setMaximumWidth(100)  # Adjust width here
        self.end_input.setText("00:00.000")  # Set default text here
        end_layout.addWidget(self.end_input)

        end_button = QtWidgets.QPushButton("Apply")
        end_button.clicked.connect(self.apply_end)
        end_layout.addWidget(end_button)

        self.canvas.clicked.connect(self.canvas_clicked)

    def reset(self):
        # Clear canvas
        self.canvas.rect_history = []
        self.canvas.letters = []
        self.canvas.selected = []
        self.canvas.update()
        self.record = RECORD()

        # Reset input fields
        self.start_input.setText("00:00.000")
        self.end_input.setText("00:00.000")

        # Reset current key
        self.curr_key = (0, 0)
        self.curr_row = -1
        self.curr_col = -1


    def open_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)", options=options)
        if filename:
            self.reset()
            self.record.import_csv(filename)
        self.canvas.update_history(self.record.history, self.record.history_key)
        self.canvas.update()

    def apply_start(self):
        start_text = self.start_input.text()
        temp = (time2sec(start_text),self.curr_key[1])
        self.curr_key = temp
        self.record.history[self.curr_row][self.curr_col] = temp
        self.canvas.update_history(self.record.history, self.record.history_key)
        self.canvas.update()
        self.start_input.setText(sec2time(self.curr_key[0]))

    def apply_end(self):
        end_text = self.end_input.text()
        temp = (self.curr_key[0],time2sec(end_text))
        print(f"self.curr_key[0] : {self.curr_key[0]}")
        self.curr_key = temp
        self.record.history[self.curr_row][self.curr_col] = temp
        self.canvas.update_history(self.record.history, self.record.history_key)
        self.canvas.update()
        self.end_input.setText(sec2time(self.curr_key[1]))

    def canvas_clicked(self, row, col):
        self.curr_key = self.record.history[row][col]
        press_time = self.curr_key[0]
        release_time = self.curr_key[1]
        self.start_input.setText(sec2time(press_time))
        self.end_input.setText(sec2time(release_time))
        print(f"press_time : {press_time} , release_time : {release_time}")
        self.curr_row = row
        self.curr_col = col
        self.canvas.update()

    def save_file_dialog(self):
        options = QtWidgets.QFileDialog.Options()
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv)", options=options)
        if filename:
            self.record.convert_to_csv(filename)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
