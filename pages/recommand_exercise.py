import sys
import multiprocessing as mp
from functools import partial

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5 import uic

from module.frame_module import TitleFrame, RecommandVideoFrame
from static.main import btn_style


class RecommandExerciseWindow(QWidget):

    btn_dict = {}

    def __init__(self, parent, page_queue):

        super(RecommandExerciseWindow, self).__init__(parent)

        self.page_queue = page_queue

        self.title_frame = TitleFrame()
        self.title_frame.setUI('추천 운동', '추천된 운동 영상을 보시고 따라 해보세요.')

    def setUI(self):
        # clear_layout(self, self.gridLayout_6)

        # for key in btn_style['운동프로그램'].keys():
    #     frame, btn, title = RecommandVideoFrame()
    #     self.btn_dict[i] = btn
    #     self.btn_dict[i].clicked.connect(partial(self.btn_click, title))
    #
    # def btn_click(self, title):
    #