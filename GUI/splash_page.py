from PySide2.QtWidgets import *
from PySide2.QtGui import *


class SplashPage(QWidget):
    def __init__(self):
        super().__init__()

        self.security_code_message = QLabel('Enter Security Code',self)
        self.ipt_box = QLineEdit(self)
        self.submit_button = QPushButton('Submit',self)

        self.security_code_message.move(301,170)
        self.ipt_box.move(301,315)
        self.submit_button.move(800,405)
        