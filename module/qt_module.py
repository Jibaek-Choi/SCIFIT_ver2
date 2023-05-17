from PyQt5.QtWidgets import *
from PyQt5 import uic

# qt 레이아웃 클리어
def clear_layout(self, layout):
    try:
        if layout is not None:
            while layout.count() > 0:
                item = layout.takeAt(0)
                w = item.widget()
                if w is not None:
                    w.deleteLater()
                else:
                    clear_layout(item.layout())
            # sip.delete(layout)
    except Exception as e:
        print(e)

def message_event_nomal(self, topic, sentence):
    QMessageBox.information(self, topic, sentence, QMessageBox.Ok, QMessageBox.Ok)