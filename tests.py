import pytest
from pytestqt.qtbot import QtBot
from app import MyWindow
from PySide2.QtCore import Qt
from matplotlib.testing.compare import compare_images
ref_images_path = "./images/test_images/ref_images/"
output_images_path = "./images/test_images/output_images/"

@pytest.fixture
def app(qtbot:QtBot):
    window = MyWindow()
    window.show()
    qtbot.addWidget(window)
    return window

def test_correct_btnclick_input(app:MyWindow,qtbot:QtBot):
    qtbot.mouseClick(app.eqn,Qt.LeftButton)
    qtbot.mouseClick(app.btn_X,Qt.LeftButton)
    qtbot.mouseClick(app.btn_pow,Qt.LeftButton)
    qtbot.mouseClick(app.keypad[2],Qt.LeftButton)
    qtbot.mouseClick(app.min,Qt.LeftButton)
    qtbot.mouseClick(app.keypad[0],Qt.LeftButton)
    qtbot.mouseClick(app.max,Qt.LeftButton)
    qtbot.mouseClick(app.keypad[4],Qt.LeftButton)
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    ref_image_name = "X_Squared.png"
    output_image_name = "btnclick_case.png"
    app.fig.savefig(output_images_path+output_image_name)
    assert compare_images(ref_images_path+ref_image_name,output_images_path+output_image_name,0.1) == None

def test_correct_keypress_input(app:MyWindow,qtbot:QtBot):
    qtbot.mouseClick(app.eqn,Qt.LeftButton)
    qtbot.keyPress(app,Qt.Key_2)
    qtbot.keyPress(app,Qt.Key_X)
    qtbot.keyPress(app,Qt.Key_Minus)
    qtbot.keyPress(app,Qt.Key_E)
    qtbot.keyPress(app,Qt.Key_AsciiCircum)
    qtbot.keyPress(app,Qt.Key_X)
    qtbot.mouseClick(app.min,Qt.LeftButton)
    qtbot.keyPress(app,Qt.Key_0)
    qtbot.mouseClick(app.max,Qt.LeftButton)
    qtbot.keyPress(app,Qt.Key_4)
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    ref_image_name = "2X_minus_expX.png"
    output_image_name = "keypress_case.png"
    app.fig.savefig(output_images_path+output_image_name)
    assert compare_images(ref_images_path+ref_image_name,output_images_path+output_image_name,0.1) == None

def test_limits(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("(2X-2)^2/(X-1)^2")
    app.min.setText("-5")
    app.max.setText("5")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    ref_image_name = "4.png"
    output_image_name = "limits_case.png"
    app.fig.savefig(output_images_path+output_image_name)
    assert compare_images(ref_images_path+ref_image_name,output_images_path+output_image_name,0.1) == None

def test_10_over_x(app:MyWindow,qtbot:QtBot):
    qtbot.mouseClick(app.eqn,Qt.LeftButton)
    qtbot.keyPress(app,Qt.Key_1)
    qtbot.keyPress(app,Qt.Key_0)
    qtbot.keyPress(app,Qt.Key_Slash)
    qtbot.keyPress(app,Qt.Key_X)
    app.min.setText("-5")
    app.max.setText("5")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    ref_image_name = "ten_over_X.png"
    output_image_name = "ten_over_X_case.png"
    app.fig.savefig(output_images_path+output_image_name)
    assert compare_images(ref_images_path+ref_image_name,output_images_path+output_image_name,0.1) == None

def test_backspace(app:MyWindow,qtbot:QtBot):
    qtbot.mouseClick(app.eqn,Qt.LeftButton)
    qtbot.keyPress(app,Qt.Key_1)
    qtbot.keyPress(app,Qt.Key_Backspace)
    qtbot.keyPress(app,Qt.Key_2)
    qtbot.keyPress(app,Qt.Key_X)
    app.min.setText("0")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    ref_image_name = "2X.png"
    output_image_name = "backspace_case.png"
    app.fig.savefig(output_images_path+output_image_name)
    assert compare_images(ref_images_path+ref_image_name,output_images_path+output_image_name,0.1) == None

def test_incorrect_eqn_unbalanced_brackets(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("(X-2))")
    app.min.setText("0")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "Unbalanced brackets"
    app.error_msg.close()

def test_incorrect_eqn_dangling_operator(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("X+2+")
    app.min.setText("0")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "Invalid syntax near +"
    app.error_msg.close()

def test_empty_eqn(app:MyWindow,qtbot:QtBot):
    app.min.setText("0")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "No Function is provided"
    app.error_msg.close()

def test_empty_min(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("X-2")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "Invalid range: min is empty"
    app.error_msg.close()

def test_incorrect_min(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("X-2")
    app.min.setText("-.")
    app.max.setText("4")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "Invalid range: Invalid min value"
    app.error_msg.close()

def test_min_not_smaller_than_max(app:MyWindow,qtbot:QtBot):
    app.eqn.setText("X-2")
    app.min.setText("4")
    app.max.setText("0")
    qtbot.mouseClick(app.btn_plot,Qt.LeftButton)
    assert app.error_msg.text() == "Invalid range: min must be smaller than max"
    app.error_msg.close()