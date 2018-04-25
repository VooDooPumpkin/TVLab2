import sys
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from mainwindow import Ui_Dialog


# combinatoric formuls
class combinatorics():

    # factorial
    def fac(r, l=1):
        if (r == 0):
            return 1
        if (l == r):
            return l
        mid = (r + l) // 2
        return combinatorics.fac(mid, l) * combinatorics.fac(r, mid + 1)

    # combinations without repetition
    def combiNoRep(n, m):
        return combinatorics.fac(n) // (combinatorics.fac(m) * combinatorics.fac(n - m))

    # combinations with repetition
    def combiRep(n, m):
        return combinatorics.combiNoRep(n + m - 1, m)

    # accommodation without repetition
    def accomNoRep(n, m):
        return combinatorics.fac(n) // combinatorics.fac(n - m)

    # accommodation with repetition
    def accomRep(n, m):
        return n ** m

    # permutation with repetition
    def permWithRep(n, arrayM):
        res = 1
        for it in arrayM:
            res *= combinatorics.fac(int(it))
        return combinatorics.fac(n) // res

    # sum of array
    def sumArray(array):
        res = 0
        for it in array:
            res += int(it)
        return res


# window
class AppWindow(QDialog):

    # prepare window
    def __init__(self):



        # init window
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        #prep
        self.ui.tabWidget.setCurrentIndex(0)

        if self.ui.q6Value.isVisible() == True:
            self.ui.q6Value.setVisible(False)
        if self.ui.label_12.isVisible() == True:
            self.ui.label_12.setVisible(False)

        self.ui.formulTab.setPixmap(QPixmap(str(1) + '.jpg').scaled(QSize(600, 100)))

        self.idxScheme = 0
        self.idxVar = 0

        self.ui.showSchemeFirst.setPixmap(QPixmap('0scheme.png').scaled(QSize(600, 200)))
        self.ui.showFormulaFirst.setPixmap(QPixmap('0formula.png').scaled(QSize(600, 100)))


        # connects
        self.ui.chooseScheme.activated[int].connect(self.schemeChanged)
        self.ui.buttonFirst.clicked.connect(lambda: self.buttonFirstPressed())
        self.ui.variantIdx.activated[int].connect(self.problemChanged)
        self.ui.buttonTab.clicked.connect(lambda: self.solveProblem())

       # self.ui.chooseLang.activated[int].connect(self.langChanged)
       # self.ui.buttonTab.clicked.connect(lambda: self.tabPressed())
    def buttonFirstPressed(self):
        q1 = self.ui.q1Value.value()
        q2 = self.ui.q2Value.value()
        q3 = self.ui.q3Value.value()
        q4 = self.ui.q4Value.value()
        q5 = self.ui.q5Value.value()
        q6 = self.ui.q6Value.value()
        p1 = 1 - q1
        p2 = 1 - q2
        p3 = 1 - q3
        p4 = 1 - q4
        p5 = 1 - q5
        p6 = 1 - q6
        if(self.idxScheme == 0):
            res = (q1 + q4 - q1*q4) * (q2 + q5 - q2*q5) * q3
        else:
            res = p1*(p2+p4*p5*p6*q2)*p3
        self.ui.resFirst.setValue(res)
    def schemeChanged(self, idx):
        self.idxScheme = idx
        if idx == 0:
            if self.ui.q6Value.isVisible() == True:
                self.ui.q6Value.setVisible(False)
            if self.ui.label_12.isVisible() == True:
                self.ui.label_12.setVisible(False)
        else:
            if self.ui.q6Value.isVisible() == False:
                self.ui.q6Value.setVisible(True)
            if self.ui.label_12.isVisible() == False:
                self.ui.label_12.setVisible(True)
        self.ui.showSchemeFirst.setPixmap(QPixmap(str(self.idxScheme) + 'scheme.png').scaled(QSize(600, 200)))
        self.ui.showFormulaFirst.setPixmap(QPixmap(str(self.idxScheme) + 'formula.png').scaled(QSize(600, 100)))

    def problemChanged(self, idx):
        self.idxVar = idx
        self.ui.formulTab.setPixmap(QPixmap(str(idx + 1) + '.jpg').scaled(QSize(600, 100)))

    def solveProblem(self):
        m1 = self.ui.m1Tab.value()
        m2 = self.ui.m2Tab.value()
        n = self.ui.nTab.value()
        p1 = m1/n
        p2 = m2/n
        q1 = 1 - p1
        q2 = 1 - p2
        if (self.idxVar == 0):
            res = ((3 * p1**2 * q1 + p1**3)/combinatorics.combiNoRep(n, 3)) * ((3 * p2**2 *q2 + p2**3)/combinatorics.combiNoRep(n,3))
        elif (self.idxVar == 1):
            res = ((3 * p1**2 * q1 + p1**3)/combinatorics.combiNoRep(n, 3)) * (1 - (3 * p2**2 *q2 + p2**3)/combinatorics.combiNoRep(n,3))
        elif (self.idxVar == 2):
            res = ((3 * p1**2 * q1 + p1**3)/combinatorics.combiNoRep(n, 3)) * (1 - (3 * p2**2 *q2 + p2**3)/combinatorics.combiNoRep(n,3)) + (1 - (3 * p1 ** 2 * q1 + p1 ** 3) / combinatorics.combiNoRep(n, 3)) * ((3 * p2 ** 2 * q2 + p2 ** 3) / combinatorics.combiNoRep(n, 3))
        elif (self.idxVar == 3):
            res = ((3 * p1**2 * q1 + p1**3)/combinatorics.combiNoRep(n, 3)) + ((3 * p2**2 *q2 + p2**3)/combinatorics.combiNoRep(n,3))
        self.ui.resultTab.setText(str(res))




# show window
app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
