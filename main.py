from PySide2.QtWidgets import *
from PySide2.QtGui import *
import splash_page
import voting_page
import review_page

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.posts = {'Head Boy':('Dog','Cat'),'Head Girl':('Monkey','Fish')}
        self.pointers = []

        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.showFullScreen()

        self.stk = QStackedWidget()

        self.sp_init()
        self.vp_init()
        
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

    def vp_button_connector(self,vp):
        vp.submit_button.clicked.connect(self.nxt_for_vp)

    def nxt(self):
        self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))

    def nxt_for_vp(self):
        #print(self.stk.currentWidget())
        button_of_person_voted_for = self.stk.currentWidget().btn_grp.checkedButton()
        name = 0
        for x in self.stk.currentWidget().candidate_list:
            if x.button is button_of_person_voted_for:
                name = x.name
        self.pointers.append([self.stk.currentIndex(),self.stk.currentWidget().post,name])
        
        if self.stk.currentIndex() == len(self.posts):
            self.rp_init()

        self.stk.setCurrentIndex(1+int(self.stk.currentIndex()))

app = QApplication()
window = MainWindow()
window.show()
app.exec_()

