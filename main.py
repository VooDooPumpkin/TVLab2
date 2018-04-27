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

        # set validator to arrayM
        reg_ex = QRegExp("(\d{1}([\.]{1}\d{1,5})? {1})*")
        reg_ex2 = QRegExp("(\d{1,5} {1})*")
        validatorArrayHi = QRegExpValidator(reg_ex, self.ui.Hi)
        validatorArrayHiA = QRegExpValidator(reg_ex, self.ui.HiA)
        validatorOutH = QRegExpValidator(reg_ex2, self.ui.lineEdit_3)
        self.ui.Hi.setValidator(validatorArrayHi)
        self.ui.HiA.setValidator(validatorArrayHiA)
        self.ui.lineEdit_3.setValidator(validatorOutH)


        if self.ui.q6Value.isVisible() == True:
            self.ui.q6Value.setVisible(False)
        if self.ui.label_12.isVisible() == True:
            self.ui.label_12.setVisible(False)

        self.ui.formulTab.setPixmap(QPixmap(str(1) + '.jpg').scaled(QSize(600, 100)))

        #Выбор схемы
        self.idxScheme = 0

        #выбор задачи
        self.idxVar = 0

        #pictures init
        self.ui.showSchemeFirst.setPixmap(QPixmap('0scheme.png').scaled(QSize(600, 200)))
        self.ui.showFormulaFirst.setPixmap(QPixmap('0formula.png').scaled(QSize(600, 100)))
        self.ui.formula_label.setPixmap(QPixmap('0formula3t.jpg').scaled(QSize(600, 100)))

        # connects
        self.ui.chooseScheme.activated[int].connect(self.schemeChanged)
        self.ui.buttonFirst.clicked.connect(lambda: self.buttonFirstPressed())
        self.ui.variantIdx.activated[int].connect(self.problemChanged)
        self.ui.buttonTab.clicked.connect(lambda: self.solveProblem())
        self.ui.chooseFormula.activated[int].connect(self.formulaChanged)
        self.ui.pushButton.clicked.connect(lambda: self.solveBayesAndFull())

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


    #Baes and full probability
    #formula choose
    def formulaChanged(self, idx):
        self.ui.formula_label.setPixmap(QPixmap(str(idx) + 'formula3t.jpg').scaled(QSize(600, 100+50*idx)))
        if idx == 0:
            if self.ui.checkBox.isVisible() == True:
                self.ui.checkBox.setVisible(False)
            if self.ui.label_16.isVisible() == True:
                self.ui.label_16.setVisible(False)
            if self.ui.lineEdit_3.isVisible() == True:
                self.ui.lineEdit_3.setVisible(False)
        else:
            if self.ui.checkBox.isVisible() == False:
                self.ui.checkBox.setVisible(True)
            if self.ui.label_16.isVisible() == False:
                self.ui.label_16.setVisible(True)
            if self.ui.lineEdit_3.isVisible() == False:
                self.ui.lineEdit_3.setVisible(True)

    #full probability solve
    def Full(self, arrayHi, arrayHiA):
        res = 1
        for i in range(len(arrayHi)):
            res *= float(arrayHi[i]) * float(arrayHiA[i])
        return res

    #Bayes solve
    def Bayes(self, arrayHi, arrayHiA, A):
        res = self.Full(arrayHi, arrayHiA)
        res /= float(A)
        return res

    #check sum of P(Hi)
    def checkPSum(self, arrayP):
        sumP = 0
        for i in range(len(arrayP)):
            sumP += float(arrayP[i])
        if sumP == 1:
            return True
        else:
            return False

    #check all PHi(A)
    def checkAllPHiA(self, arrayHiA):
        for i in range(len(arrayHiA)):
            if int(arrayHiA[i]) > 1 or int(arrayHiA[i]) < 0:
                return False
            else:
                return True

    #Solve Bayes and full probability
    def solveBayesAndFull(self):
        # parse text
        string = self.ui.Hi.text()
        arrayHi = string.split()
        string = self.ui.HiA.text()
        arrayHiA = string.split()

        #check count
        if len(arrayHi) != self.ui.spinBox.value():
            # show error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Количество вероятностей гипотез P(Hi) не равно количеству событий!')
            msg.exec_()
        elif len(arrayHiA) != self.ui.spinBox.value():
            # show error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Количество условных вероятностей гипотез PHi(A) не равно количеству событий!')
            msg.exec_()
        #check sum of P(Hi)
        elif (self.checkPSum(arrayHi) == False):
           # show error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Сумма вероятностей гипотез P(Hi) не равна единице!')
            msg.exec_()
        #check all PHi(A)
        elif self.checkAllPHiA(arrayHiA) == False:
            # show error
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText('Вероятность не может быть меньше нуля или больше единицы!')
            msg.exec_()
        # show result
        else:
            if self.ui.chooseFormula.currentIndex() == 0:
                self.ui.textBrowser.setText(str(self.Full(arrayHi, arrayHiA)))
            else:
                if self.ui.checkBox.isChecked():
                    string = self.ui.lineEdit_3.text()
                    outH = string.split()
                    if len(outH) > self.ui.spinBox.value():
                        # show error
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Warning)
                        msg.setText('Количество выбранных гипотез PHi(A) больше количества событий!')
                        msg.exec_()
                    else:
                        err = False
                        string = ''
                        for i in range(len(outH)):
                            if int(outH[i]) > self.ui.spinBox.value():
                                # show error
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Warning)
                                msg.setText('Не существует гипотезы с номером ' + str(outH[i]) + '!')
                                msg.exec_()
                                err = True
                            else:
                                string += 'P(H' + str(outH[i]) + ') = ' + str(self.Bayes(arrayHi, arrayHiA, arrayHi[int(outH[i])-1])) + '; '
                        if err != True:
                            self.ui.textBrowser.setText(string)
                else:
                    string = ''
                    for i in range(self.ui.spinBox.value()):
                        string += 'P(H' + str(i+1) + ') = ' + str(self.Bayes(arrayHi, arrayHiA, arrayHi[i])) + '; '
                    self.ui.textBrowser.setText(string)


# show window
app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
