import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
import StyleSheets as ss
from UiMainview import Ui_MainWindow
import accept_drop_tab_and_text_edit.Common as common

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.setWindowTitle("Lens TE")
        self.ui.setupUi(self)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.title_bar_widgets_dict["minimize_button"].clicked.connect(lambda: self.showMinimized())
        self.ui.title_bar_widgets_dict["maximize_button"].clicked.connect(lambda: self.maximizeAndRestore())
        self.ui.title_bar_widgets_dict["exit_button"].clicked.connect(lambda: self.close())

        def moveWindow(event):
            if self.isMaximized():
                return
            else:
                if event.buttons() == QtCore.Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

        self.ui.title_bar_widgets_dict["title_bar_move_frame"].mouseMoveEvent = moveWindow

    def maximizeAndRestore(self):
        if self.isMaximized():
            self.showNormal()
            maximize_icon = QtGui.QIcon()
            maximize_icon.addPixmap(QtGui.QPixmap("main_window_icons/MaximizeButtonicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.title_bar_widgets_dict["maximize_button"].setIcon(maximize_icon)
            self.ui.title_bar_widgets_dict["exit_button"].setStyleSheet(ss.exit_button_stylesheet_window_normal)
            self.ui.title_bar_frame.setStyleSheet(ss.title_bar_frame_stylesheet_window_normal)
        else:
            self.showMaximized()
            restore_icon = QtGui.QIcon()
            restore_icon.addPixmap(QtGui.QPixmap("main_window_icons/RestoreButtonicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.title_bar_widgets_dict["maximize_button"].setIcon(restore_icon)
            self.ui.title_bar_widgets_dict["exit_button"].setStyleSheet(ss.exit_button_stylesheet_window_maximized)
            self.ui.title_bar_frame.setStyleSheet(ss.title_bar_frame_stylesheet_window_maximized)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        self.maximizeAndRestore()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_app_id = 'Lens TE'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)
    font_id = QtGui.QFontDatabase.addApplicationFont("fonts/Consolas.ttf")
    _fontstr = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
    _font = QtGui.QFont(_fontstr, 10)
    app.setFont(_font)
    main_window = MainWindow()
    common.connect(main_window)
    main_window.show()
    sys.exit(app.exec_())