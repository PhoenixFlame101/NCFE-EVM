from PySide2.QtWidgets import *
from PySide2.QtGui import *

class ReviewPage(QWidget):
    def __init__(self,summary):
        super().__init__()

        self.summary = summary
        self.table = QTableWidget(self,'REVIEW')
        self.table.setColumnCount(2)
        self.table.setVerticalHeaderLabels(['Post','Name'])
        self.table.setRowCount(len(self.summary))
        for x in self.summary:
            num = x[0]
            post  = x[1]
            name = x[2]
            self.table.setItem(num-1,0,QTableWidgetItem(post))
            self.table.setItem(num-1,1,QTableWidgetItem(name))

        self.submit_button = QPushButton('Submit',self)

        self.lay = QVBoxLayout()
        self.lay.addWidget(self.table)
        self.lay.addWidget(self.submit_button)

        self.setLayout(self.lay)

'''
app = QApplication([])
wind = ReviewPage([[1,'Head boy','Sanjay'],[2,'Head girl','Sanjayana']])
wind.show()
app.exec_()
'''