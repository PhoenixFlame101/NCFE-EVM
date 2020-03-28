from PySide2.QtWidgets import *
from PySide2.QtGui import *

class Candidate(QWidget):
    def __init__(self,name):
        super().__init__()

        self.name = name
        self.clicked = False
        #self.picture = picture
        
        #for the pic
        '''
        pic_label = QLabel(self)
        pixmap = QPixmap(self.picture)
        pic_label.setPixmap(pixmap)
        '''

        self.name_label = QLabel(self.name,self)
        self.button = QRadioButton(self)

        #self.pic_label.setGeometry(10,10,300,300)
        self.name_label.move(150,315)
        self.button.move(200,330)

        self.button.toggled.connect(lambda:self.clicked_func(self.button))

    def clicked_func(self,b):
        if b.isChecked() == True:
            self.clicked = True
        elif b.isChecked() == False:
            self.clicked = False

class VotingPage(QWidget):
    def __init__(self,post,clist):#Each candidate in the clist should be a (name,later picture)
        super().__init__()    

        self.post = post
        self.clist = clist
        self.voted_for = 0
        self.candidate_list = []

        self.vert_layout = QVBoxLayout()

        self.generate_candidates()
        self.candidate_group_box = QGroupBox(self.post)
        self.candidate_hbox = QHBoxLayout()
        self.put_candidates_in_the_layout()
        self.submit_button = QPushButton('Next page')
        self.vert_layout.addWidget(self.candidate_group_box)
        self.vert_layout.addWidget(self.submit_button)
        self.setLayout(self.vert_layout)

        self.btn_grp = QButtonGroup()
        self.make_button_group()

    def generate_candidates(self):
        for x in self.clist:
            self.candidate_list.append(Candidate(x))#Here when you add the picture then make it candidate[1]

    def put_candidates_in_the_layout(self):
        for x in self.candidate_list:
            self.candidate_hbox.addWidget(x)
        self.candidate_group_box.setLayout(self.candidate_hbox)

    def make_button_group(self):
        for x in self.candidate_list:
            self.btn_grp.addButton(x.button)
        self.btn_grp.setExclusive(True)
'''
app = QApplication([])
wind = VotingPage('POST',['hi','hello','heuyy'])
wind.show()
app.exec_()
'''