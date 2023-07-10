import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget,QPushButton,QTextEdit
from PySide2.QtGui import QFont,QKeyEvent
from PySide2.QtCore import Qt
class MyWindow(QWidget):
    allowed_set:set = {Qt.Key_0,Qt.Key_1,Qt.Key_2,Qt.Key_3,Qt.Key_4,Qt.Key_5,Qt.Key_6,Qt.Key_7,Qt.Key_8,Qt.Key_9,Qt.Key_Plus,Qt.Key_Minus,Qt.Key_Asterisk,Qt.Key_Slash,Qt.Key_AsciiCircum,Qt.Key_ParenLeft,Qt.Key_ParenRight,Qt.Key_X,Qt.Key_Backspace}
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(300,300,640,480)
        self.setFixedSize(640,480)
        self.add_keypad(375,50,30,30,40,self.keypad_click)
        self.add_text(self.text,"Enter Equation Here",25,50,300,40,QFont("Arial",18))
        self.add_text(QTextEdit(self),"Min",25,100,75,30,QFont("Arial",12))
        self.add_text(QTextEdit(self),"Max",125,100,75,30,QFont("Arial",12))
        self.add_btn(QPushButton("Plot",self),25,150,150,50,self.plot_click,QFont("Arial",18))
        fig = Figure(figsize=(5,5),dpi=100)
        self.axes = fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(fig)
    def plot_click(self):
        self.axes.clear()
        # Validate Input
        # Call the backend logic
        self.axes.plot([1,2,3,4,5],[1,2,7,4,5])
        # Plot the returned data
        self.canvas.show()
        pass
    def keypad_click(self):
        if(self.sender().text()=="del"):
            self.text.textCursor().deletePreviousChar()
        else:
            self.text.insertPlainText(self.sender().text())
    def keypress(self,e:QKeyEvent):
        if(e.key() in self.allowed_set):
            if(e.key()==Qt.Key_Backspace):
                self.text.textCursor().deletePreviousChar()
            else:
                self.text.insertPlainText(e.text())
    def add_btn(self,btn:QPushButton,x,y,w,h,func,font:QFont = QFont("Arial",12)):
        btn.move(x,y)
        btn.setFixedSize(w,h)
        btn.clicked.connect(func)
        btn.setFont(font)
    def add_text(self,text:QTextEdit,placeholder:str,x,y,w,h,font:QFont):
        text.move(x,y)
        text.setFixedSize(w,h)
        text.setPlaceholderText(placeholder)
        text.setFont(font)
    def add_keypad(self,x,y,w,h,step,func):
        self.keypad:list = [QPushButton("0",self)]
        hold_x = x
        hold_y = y
        for i in range(1,10):
            self.keypad.append(QPushButton(str(i),self))
            self.add_btn(self.keypad[i],x,y,w,h,func)
            x += step
            if x >= hold_x+step*3:
                x = hold_x
                y += step
        self.add_btn(self.keypad[0],x+step,y,w,h,func)
        x = hold_x+step*3 + 10
        hold_x = x
        y = hold_y
        self.btn_add = QPushButton("+",self)
        self.btn_sub = QPushButton("-",self)
        self.btn_mul = QPushButton("*",self)
        self.btn_div = QPushButton("/",self)
        self.btn_exp = QPushButton("^",self)
        self.btn_var = QPushButton("X",self)
        self.btn_Lbrkt = QPushButton("(",self)
        self.btn_Rbrkt = QPushButton(")",self)
        self.btn_del = QPushButton("del",self)
        self.text = QTextEdit(self)
        self.text.keyPressEvent = self.keypress
        self.add_btn(self.btn_add,x,y,30,30,self.keypad_click)
        self.add_btn(self.btn_mul,x,y+step,30,30,self.keypad_click)
        self.add_btn(self.btn_exp,x,y+step*2,30,30,self.keypad_click)
        self.add_btn(self.btn_sub,x+step,y,30,30,self.keypad_click)
        self.add_btn(self.btn_div,x+step,y+step,30,30,self.keypad_click)
        self.add_btn(self.btn_var,x+step,y+step*2,30,30,self.keypad_click,QFont("Cambria Math",12))
        self.add_btn(self.btn_Lbrkt,x+step*2,y,30,30,self.keypad_click)
        self.add_btn(self.btn_Rbrkt,x+step*2,y+step,30,30,self.keypad_click)
        self.add_btn(self.btn_del,x+step*2,y+step*2,30,30,self.keypad_click)