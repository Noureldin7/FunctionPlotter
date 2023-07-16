import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget,QPushButton,QTextEdit,QMessageBox,QApplication,QMainWindow
from PySide2.QtGui import QFont,QKeyEvent,QTextCursor
from PySide2.QtCore import Qt
from validate import validate
from plotter import config
from function_parser import parse,nums
nums = nums.union({'-'})
class MyWindow(QMainWindow):
    misc_set:set = {Qt.Key_Left,Qt.Key_Right,Qt.Key_Plus,Qt.Key_Minus,Qt.Key_Asterisk,Qt.Key_Slash,Qt.Key_AsciiCircum,Qt.Key_ParenLeft,Qt.Key_ParenRight,Qt.Key_X,Qt.Key_Backspace}
    num_set:set = {Qt.Key_0,Qt.Key_1,Qt.Key_2,Qt.Key_3,Qt.Key_4,Qt.Key_5,Qt.Key_6,Qt.Key_7,Qt.Key_8,Qt.Key_9,Qt.Key_Period,Qt.Key_Minus,Qt.Key_E}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setFixedSize(800,600)
        self.move(300,50)
        self.build_gui()
        QApplication.instance().focusChanged.connect(self.update_focused)
        self.fig = Figure(figsize=(6.7,4),dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.fig)
        config(self.axes)
        self.canvas.setParent(self)
        self.canvas.move(75,180)
        self.toolbar = NavigationToolbar2QT(self.canvas,self.canvas)
        self.curves = None

    def plot_click(self):
        eqn_string = self.eqn.toPlainText()
        min_string = self.min.toPlainText()
        max_string = self.max.toPlainText()
        # Validate Input
        valid, msg, eqn_string = validate(eqn_string,min_string,max_string)
        if valid:
            # Call the backend logic
            x,y = parse(eqn_string,float(min_string),float(max_string))
            if self.curves == None:
                config(self.axes,(x[0],x[-1]),(min(y),max(y)))
            else:
                self.curves.pop(0).remove()
            # Plot the returned data
            self.curves = self.axes.plot(x,y,color='r')
            self.canvas.draw()
        else:
            self.error_msg = QMessageBox()
            self.error_msg.setWindowTitle("Error")
            self.error_msg.setText(msg)
            self.error_msg.show()

    def key_click(self):
        if(self.sender().text()=="←"):
            self.focused.textCursor().deletePreviousChar()
        elif self.sender().text() in nums or self.focused==self.eqn:
            self.focused.insertPlainText(self.sender().text())

    def key_press(self,e:QKeyEvent):
        match e.key():
            case Qt.Key_Left:
                self.focused.moveCursor(QTextCursor.Left)
            case Qt.Key_Right:
                self.focused.moveCursor(QTextCursor.Right)
            case Qt.Key_Backspace:
                self.focused.textCursor().deletePreviousChar()
            case Qt.Key_Delete:
                self.focused.textCursor().deleteChar()
            case _:
                if e.key() in self.num_set:
                    self.focused.insertPlainText(e.text().lower())
                elif e.key() in self.misc_set and self.focused==self.eqn:
                    self.focused.insertPlainText(e.text().upper())

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

    def build_gui(self):
        x = 500
        y = 25
        w,h = 30,30
        step = 40
        self.build_keypad(x,y,w,h,step,self.key_click)
        x = x+step*3+10
        self.build_misc(x,y,w,h,step,self.key_click)
        self.build_texts()
        self.btn_plot = QPushButton("Plot",self)
        self.add_btn(self.btn_plot,75,125,150,50,self.plot_click,QFont("Arial",18))

    def build_misc(self,x,y,w,h,step,func):
        self.btn_add = QPushButton("+",self)
        self.btn_sub = QPushButton("-",self)
        self.btn_mul = QPushButton("*",self)
        self.btn_div = QPushButton("/",self)
        self.btn_pow = QPushButton("^",self)
        self.btn_X = QPushButton("X",self)
        self.btn_Lbrkt = QPushButton("(",self)
        self.btn_Rbrkt = QPushButton(")",self)
        self.btn_del = QPushButton("←",self)
        self.add_btn(self.btn_add,x,y,w,h,func)
        self.add_btn(self.btn_mul,x,y+step,w,h,func)
        self.add_btn(self.btn_pow,x,y+step*2,w,h,func)
        self.add_btn(self.btn_sub,x+step,y,w,h,func)
        self.add_btn(self.btn_div,x+step,y+step,w,h,func)
        self.add_btn(self.btn_X,x+step,y+step*2,w,h,func,QFont("Cambria Math",12))
        self.add_btn(self.btn_Lbrkt,x+step*2,y,w,h,func)
        self.add_btn(self.btn_Rbrkt,x+step*2,y+step,w,h,func)
        self.add_btn(self.btn_del,x+step*2,y+step*2,w,h,func,QFont("Cambria Math",12))

    def build_keypad(self,x,y,w,h,step,func):
        self.keypad:list = [QPushButton("0",self)]
        hold_x = x
        for i in range(1,10):
            self.keypad.append(QPushButton(str(i),self))
            self.add_btn(self.keypad[i],x,y,w,h,func)
            x += step
            if x >= hold_x+step*3:
                x = hold_x
                y += step
        self.add_btn(self.keypad[0],x,y,w,h,func)
        self.btn_dot = QPushButton(".",self)
        self.btn_e = QPushButton("e",self)
        self.add_btn(self.btn_dot,x+step,y,w,h,func,QFont("Cambria Math",12))
        self.add_btn(self.btn_e,x+step*2,y,w,h,func)

    def build_texts(self):
        self.eqn = QTextEdit(self)
        self.min = QTextEdit(self)
        self.max = QTextEdit(self)
        self.focused = self.eqn
        self.keyPressEvent = self.key_press
        self.eqn.keyPressEvent = self.key_press
        self.min.keyPressEvent = self.key_press
        self.max.keyPressEvent = self.key_press
        self.add_text(self.eqn,"Enter Equation Here",75,25,300,40,QFont("Arial",18))
        self.add_text(self.min,"Min",75,75,75,30,QFont("Arial",12))
        self.add_text(self.max,"Max",175,75,75,30,QFont("Arial",12))
        
    def update_focused(self,e):
        if not isinstance(self.focusWidget(),QPushButton):
            self.focused = self.focusWidget()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())