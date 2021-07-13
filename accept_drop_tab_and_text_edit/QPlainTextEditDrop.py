from PyQt5 import QtCore, QtGui, QtWidgets
import accept_drop_tab_and_text_edit.Common as common
import os

class QPlainTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self,parentwidget):
        super(QPlainTextEdit, self).__init__(parentwidget)    
        self.setAcceptDrops(True)
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()        
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.ignore()
            for url in event.mimeData().urls():
                file_to_open = str(url.toLocalFile())
                with open(file_to_open, 'r') as f:
                    data = f.read()
                    common.main_window.ui.newTab(data,os.path.basename(file_to_open))
                    f.close()
        else:
            event.ignore()