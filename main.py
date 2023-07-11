from my_window import MyWindow
from PySide2.QtWidgets import QApplication
import sys
app = QApplication(sys.argv)
win = MyWindow(app)
win.show()
sys.exit(app.exec_())
