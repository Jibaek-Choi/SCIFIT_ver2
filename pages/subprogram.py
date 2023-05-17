import sys
import multiprocessing as mp
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import uic

from static.main import btn_style, subprogram


class SubProgramWindow(QWidget):


    def __init__(self, parent, page_queue):
        super(SubProgramWindow, self).__init__(parent)

        self.page_queue = page_queue

    def setUI(self):
        # clear_layout(self, self.gridLayout_6)

        label = QLabel()
        # label.setStyleSheet()
        label.setFixedHeight(709)
        label.setFixedWidth(946)


        # for key in btn_style['운동프로그램'].keys():


    def set_layout(self, btn_list):
        info = subprogram

        for i in btn_list:
            info = info[i]

        if len(btn_list) > 1:
            pass
        else:
            pass

    def make_button(self, i, data):
        button = QPushButton()
        button.setStyleSheet(btn_style[data][i])
        button.setFixedWidth(472)
        button.setFixedHeight(402)
        button.clicked.connect(partial(self.btn_click, i))

        return button

    def btn_click(self, i):
        self.page_queue.put(self.page_info[i])