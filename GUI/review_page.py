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
            num = x
            post  = self.summary[x][0]
            name = self.summary[x][1]
            self.table.setItem(num-1,0,QTableWidgetItem(post))
            self.table.setItem(num-1,1,QTableWidgetItem(name))

        self.submit_button = QPushButton('Submit',self)

        self.lay = QVBoxLayout()
        self.lay.addWidget(self.table)
        self.lay.addWidget(self.submit_button)

        self.button_box_list = []
        for x in range(len(self.summary)):
            self.button_box_list.append(QPushButton('ChangeVote'))
        self.button_box = QVBoxLayout()
        for x in self.button_box_list:
            self.button_box.addWidget(x)
        self.total_lay = QHBoxLayout()
        self.total_lay.addLayout(self.lay)
        self.total_lay.addLayout(self.button_box)

        self.setLayout(self.total_lay)

    def update(self):
        for x in self.summary:
            num = x
            post  = self.summary[x][0]
            name = self.summary[x][1]
            self.table.setItem(num-1,0,QTableWidgetItem(post))
            self.table.setItem(num-1,1,QTableWidgetItem(name))
        print('done')

'''
app = QApplication([])
wind = ReviewPage([[1,'Head boy','Sanjay'],[2,'Head girl','Sanjayana']])
wind.show()
app.exec_()
'''