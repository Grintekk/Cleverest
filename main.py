import sys
import json
import random
import time

# from PyQt5.QtGui import QPixmap, QImage
from PyQt5.Qt import QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import qApp, QPushButton, QLabel, QApplication


class AppWindow(QMainWindow):
    def __init__(self):
        super(AppWindow, self).__init__()
        self.cells_list = [i for i in range(36)]
        self.cells_dict = {}
        self.questions = {}
        self.setWindowTitle("App")
        self.left = 40
        self.top = 40
        self.width = 1850
        self.height = 950
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.timer_for_window = QTimer(self) #закрытие вопроса

        self.button_generate = QPushButton(self)
        self.button_generate.setGeometry(int(self.width/2), int(self.height - 150), 100, 50)
        self.button_generate.setText("Start")
        self.button_generate.clicked.connect(self.button_generate_collors)

        self.show_question_button = QPushButton(self)
        self.show_question_button.setText("Показать вопрос")
        self.show_question_button.setGeometry(int(self.width - 550),int(self.height/4), 100, 50)
        self.show_question_button.clicked.connect(self.create_question_window)
        self.show_question_button.setVisible(False)

        # self.text_quest = QLabel(self)
        # self.text_quest.setGeometry(int(self.width - 350),int(self.height/4), 300, 300)
        with open("questions.json", encoding="utf-8") as outfile:
            self.questions = json.load(outfile)
        self.questions_copy = self.questions.copy()

        self.cells = [QPushButton(self) for i in range(36)]
        for i in range(len(self.cells)):
            self.cells[i].clicked.connect(lambda ch, i=i: self.click_cell(i))
        self.create_cells()
        # self.timer = QTimer(self)

    def click_cell(self,number):
        self.rand = random.choice(list(self.questions[self.cells_dict[number]]))
        self.text_quest = self.questions[self.cells_dict[number]][self.rand]
        self.questions[self.cells_dict[number]].pop(self.rand)
        # self.text_quest.setText("Вопрос №"+str(number))
        #
        self.show_question_button.setVisible(True)
        self.cells[number].setStyleSheet(f"background-color: {self.cells_dict[number]}")

    def hide_cells(self):
        for i in self.cells:
            i.setStyleSheet("background-color: grey")

    def create_question_window(self):
        self.show_question_button.setVisible(False)
        self.question_window = Question_window(self)

        self.timer_for_window.timeout.connect(self.question_window.close)
        self.question_window.show()
        self.question_window.show_text(self.text_quest)
        # qApp.processEvents()
        # time.sleep(5)
        # QTimer.singleShot(5000,self.question_window.close())
        # self.question_window.close()
        self.timer_for_window.start(3000)

    def button_generate_collors(self):
        self.button_generate.setDisabled(True)
        self.gen()
        for i in range(len(self.cells)):
            qApp.processEvents()
            time.sleep(0.1)
            self.cells[i].setStyleSheet(f"background-color: {self.cells_dict[i]}")
        self.button_generate.setEnabled(True)
        self.cells_list = [i for i in range(36)]
        self.questions = self.questions_copy.copy()
        # qApp.processEvents()
        self.timer_for_window.timeout.connect(self.hide_cells)
        self.timer_for_window.start(int(self.questions["timer_for_field"]*1000))
        # time.sleep(self.questions["timer_for_field"])
        # self.hide_cells()

    def create_cells(self):
        j = 0
        left = 100
        top = 20
        for i in range(len(self.cells)):
            self.cells[i].setText(str(int(i)+1))

            self.cells[i].setGeometry(left,top,100,75)
            left += 200
            j += 1
            if j == 6:
                j = 0
                top += 120
                left = 100
        self.hide_cells()

    def gen(self):
        for i in range(10):
            a = random.choice(self.cells_list)
            self.cells_dict[a] = "red"
            self.cells_list.remove(a)
            a = random.choice(self.cells_list)
            self.cells_dict[a] = "cyan"
            self.cells_list.remove(a)
            a = random.choice(self.cells_list)
            self.cells_dict[a] = "yellow"
            self.cells_list.remove(a)
        for i in self.cells_list:
            self.cells_dict[i] = "white"
        self.cells_list.clear()


class Question_window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вопрос")
        self.resize(500,500)

        self.text_quest = QLabel(self)
        self.text_quest.setGeometry(100,100,300,300)

    def show_text(self, text):
        self.text_quest.setText(str(text))

    # def close_window(self):
    #     self.close()


def main_window():
    app = QApplication(sys.argv)
    window = AppWindow()

    window.show()
    sys.exit(app.exec_())


main_window()
