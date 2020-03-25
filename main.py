from PySide2.QtWidgets import *
from PySide2.QtGui import *
import splash_page
import voting_page
import review_page
import os
import psutil

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.posts = {'Head Boy':('Dog','Cat'),'Head Girl':('Monkey','Fish'),'Asst Head boy':('Rat','Snake')}
        self.pointers = {}

        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.showFullScreen()

        self.stk = QStackedWidget()

        self.sp_init()
        self.vp_init()
        self.added_rp = False
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.stk)
        self.cw.setLayout(vbox)

    def sp_init(self):
        self.sp = splash_page.SplashPage()
        self.stk.addWidget(self.sp)
        self.sp.submit_button.clicked.connect(self.nxt)

    def vp_init(self):
        for x in self.posts:
            vp = voting_page.VotingPage(x,list(self.posts[x]))
            self.vp_button_connector(vp)
            self.stk.addWidget(vp)

    def rp_init(self):
        rp = review_page.ReviewPage(self.pointers)
        self.stk.addWidget(rp)
        self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))
        self.connect_buttons_for_review_page()

    def connect_buttons_for_review_page(self):
        def foo(num):
            self.stk.setCurrentIndex(num)
        for i in range(len(self.pointers)):
            print(self.stk.currentWidget())
            self.stk.currentWidget().button_box_list[i].clicked.connect(foo(i+1))
            print(i)
            #btn.clicked.connect(foo(i+1))

    def vp_button_connector(self,vp):
        vp.submit_button.clicked.connect(self.nxt_for_vp)

    def nxt(self):
        self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))

    def nxt_for_vp(self):
        #print(self.stk.currentWidget())
        button_of_person_voted_for = self.stk.currentWidget().btn_grp.checkedButton()
        if button_of_person_voted_for is not None:
            name = 0
            for x in self.stk.currentWidget().candidate_list:
                if x.button is button_of_person_voted_for:
                    name = x.name
            self.pointers[self.stk.currentIndex()]=[self.stk.currentWidget().post,name]

            if self.stk.currentIndex() == len(self.posts) and self.added_rp == False:
                def foo(num):
                    self.stk.setCurrentIndex(num)
                self.rp = review_page.ReviewPage(self.pointers)
                
                #have to manually connect the buttons that are there on the review page that take the voter back to the vote change page
                self.rp.button_box_list[0].clicked.connect(lambda:self.stk.setCurrentIndex(1))
                self.rp.button_box_list[1].clicked.connect(lambda:self.stk.setCurrentIndex(2))
                self.rp.button_box_list[2].clicked.connect(lambda:self.stk.setCurrentIndex(3))

                self.stk.addWidget(self.rp)
                self.stk.setCurrentWidget(self.rp)
                self.added_rp = True
                #self.connect_buttons_for_review_page()

            elif self.stk.currentIndex() == len(self.posts) and self.added_rp == True:
                self.rp.update()
                self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))
            else:
                self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))
            
        else:
            msgbox = QMessageBox()
            msgbox.setText('You have not chosen a candidate to vote for')
            msgbox.exec_()

        print(self.pointers)

def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec_()

main()
'''
process = psutil.Process(os.getpid())
print(process.memory_info()[0])
'''