import os
import subprocess
from PyQt5 import QtCore, QtGui, QtWidgets
import StyleSheets as ss
from code_editor_and_highlighter.CodeEditorClass import *
from code_editor_and_highlighter.PythonHighlighterClass import *
from accept_drop_tab_and_text_edit.QTabWidgetDrop import *
from accept_drop_tab_and_text_edit.QPlainTextEditDrop import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setStyleSheet(ss.main_window_stylesheet)
        MainWindow.setWindowIcon((QtGui.QIcon("main_window_icons/Logoicon.png")))
        MainWindow.resize(834, 638)
        self.central_widget = QtWidgets.QWidget(MainWindow)
        ####################
        ##MAIN GRID LAYOUT##
        ####################
        self.main_grid_layout = QtWidgets.QGridLayout()
        self.main_grid_layout.setSpacing(0)
        self.main_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setLayout(self.main_grid_layout)
        ############
        ##TITLEBAR##
        ############
        self.title_bar_frame = QtWidgets.QFrame()
        self.title_bar_frame.setFixedHeight(29)
        self.title_bar_frame.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Fixed)
        self.title_bar_frame.setStyleSheet(ss.title_bar_frame_stylesheet_window_normal)
        self.title_bar_frame_horizontal_layout = QtWidgets.QHBoxLayout()
        self.title_bar_frame_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_widgets_names=["title_label","title_bar_move_frame","minimize_button","maximize_button","exit_button"]
        self.title_bar_widgets_stylesheets=[ss.minimize_button_stylesheet,ss.maximize_button_stylesheet, ss.exit_button_stylesheet_window_normal]
        self.title_bar_widgets_icons=["main_window_icons/MinimizeButtonicon.png",
        "main_window_icons/MaximizeButtonicon.png", "main_window_icons/ExitButtonicon.png"]
        self.title_bar_widgets_dict,title_bar_loop_counter={},0
        for x in self.title_bar_widgets_names:
            if x == "title_label":
                self.title_bar_widgets_dict[x] = QtWidgets.QLabel()
                self.title_bar_widgets_dict[x].setMinimumSize(QtCore.QSize(16777215, 29))
                self.title_bar_widgets_dict[x].setMaximumSize(QtCore.QSize(80, 29))
                self.title_bar_frame_horizontal_layout.addWidget(self.title_bar_widgets_dict[x])
                self.title_bar_widgets_dict[x].setStyleSheet(ss.title_label_stylesheet)
                self.title_bar_widgets_dict[x].setPixmap(QtGui.QPixmap("main_window_icons/Titleicon.png"))
            elif x == "title_bar_move_frame":
                self.title_bar_widgets_dict[x] = QtWidgets.QFrame()
                self.title_bar_widgets_dict[x].setMinimumSize(QtCore.QSize(16777215, 29))
                self.title_bar_widgets_dict[x].setMaximumSize(QtCore.QSize(16777215, 29))
                self.title_bar_widgets_dict[x].setStyleSheet(ss.title_bar_move_frame_stylesheet)
                self.title_bar_frame_horizontal_layout.addWidget(self.title_bar_widgets_dict[x])
            else:
                self.title_bar_widgets_dict[x] = QtWidgets.QPushButton(self.title_bar_frame)
                title_bar_button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                self.title_bar_widgets_dict[x].setSizePolicy(title_bar_button_size_policy)
                self.title_bar_widgets_dict[x].setStyleSheet(self.title_bar_widgets_stylesheets[title_bar_loop_counter])
                title_bar_button_icon = QtGui.QIcon()
                title_bar_button_icon.addPixmap(QtGui.QPixmap(self.title_bar_widgets_icons[title_bar_loop_counter]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.title_bar_widgets_dict[x].setIcon(title_bar_button_icon)
                self.title_bar_widgets_dict[x].setMinimumSize(QtCore.QSize(51, 29))
                self.title_bar_widgets_dict[x].setMaximumSize(QtCore.QSize(51, 29))
                if x == "maximize_button":
                    self.title_bar_widgets_dict[x].setIconSize(QtCore.QSize(18, 18))
                else:
                    self.title_bar_widgets_dict[x].setIconSize(QtCore.QSize(21, 21))
                self.title_bar_frame_horizontal_layout.addWidget(self.title_bar_widgets_dict[x])
                title_bar_loop_counter+=1
        self.title_bar_frame.setLayout(self.title_bar_frame_horizontal_layout)
        ###########
        ##TOOLBAR##
        ###########
        self.tool_bar_frame = QtWidgets.QFrame(self.central_widget)
        self.tool_bar_frame.setMinimumSize(QtCore.QSize(0, 40))
        self.tool_bar_frame.setMaximumSize(QtCore.QSize(16777215, 40))
        self.tool_bar_frame.setStyleSheet(ss.tool_bar_frame_stylesheet)
        self.tool_bar_frame_layout = QtWidgets.QHBoxLayout(self.tool_bar_frame)
        self.tool_bar_frame_layout.setContentsMargins(0, 0, 9, 0)
        self.tool_bar_frame_layout.setSpacing(0)
        self.tool_bar_widgets_names=["tool_bar_spacer_left","new_file_button","open_file_button","save_button","save_as_button",
        "tool_bar_spacer_middle","run_button","tool_bar_spacer_right"]
        self.tool_bar_widgets_icons=["main_window_icons/NewFileButtonicon.png","main_window_icons/OpenButtonicon.png",
        "main_window_icons/SaveButtonicon.png", "main_window_icons/SaveAsButtonicon.png", "main_window_icons/RunButtonicon.png"]
        self.tool_bar_buttons_methods=[lambda: self.newTab("","New File"),self.openFile,self.saveFile,self.saveFileAs,self.runCode]
        self.tool_bar_buttons_shortcuts=["Ctrl+N","Ctrl+O","Ctrl+S","Shift+S","Ctrl+B"]
        self.tool_bar_widgets_dict,tool_bar_loop_counter={},0
        for x in self.tool_bar_widgets_names:
            if "spacer" in x:
                if x == "tool_bar_spacer_middle":
                    self.tool_bar_widgets_dict[x] = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
                else:
                    self.tool_bar_widgets_dict[x] = QtWidgets.QSpacerItem(3, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
                self.tool_bar_frame_layout.addItem(self.tool_bar_widgets_dict[x])
            else:
                self.tool_bar_widgets_dict[x] = QtWidgets.QPushButton() 
                self.tool_bar_widgets_dict[x].setMinimumSize(QtCore.QSize(30, 30))
                self.tool_bar_widgets_dict[x].setMaximumSize(QtCore.QSize(30, 30))
                self.tool_bar_widgets_dict[x].setStyleSheet(ss.tool_bar_buttons_stylesheet)
                tool_bar_button_icon = QtGui.QIcon()
                tool_bar_button_icon.addPixmap(QtGui.QPixmap(self.tool_bar_widgets_icons[tool_bar_loop_counter]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                self.tool_bar_widgets_dict[x].setIcon(tool_bar_button_icon)
                self.tool_bar_widgets_dict[x].setIconSize(QtCore.QSize(30, 30))
                self.tool_bar_widgets_dict[x].clicked.connect(self.tool_bar_buttons_methods[tool_bar_loop_counter])
                self.tool_bar_widgets_dict[x].setShortcut(self.tool_bar_buttons_shortcuts[tool_bar_loop_counter])
                self.tool_bar_frame_layout.addWidget(self.tool_bar_widgets_dict[x])
                tool_bar_loop_counter+=1
        ############
        ##SPLITTER##
        ############
        self.input_output_splitter = QtWidgets.QSplitter(self.central_widget)
        self.input_output_splitter.setStyleSheet(ss.input_output_splitter_stylesheet)
        self.input_output_splitter.setOrientation(QtCore.Qt.Vertical)
        self.input_output_splitter.setOpaqueResize(True)
        self.input_output_splitter.setHandleWidth(15)
        self.input_output_splitter.setChildrenCollapsible(True)
        ##############
        ##TAB WIDGET##
        ##############
        self.files_tab_widget_layout_widget = QtWidgets.QWidget(self.input_output_splitter)
        self.files_tab_widget_layout_widget.setStyleSheet(ss.files_tab_widget_layout_widget_stylesheet)
        self.files_tab_widget_layout = QtWidgets.QGridLayout(self.files_tab_widget_layout_widget)
        self.files_tab_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.files_tab_widget_layout.setSpacing(0)
        self.files_tab_widget = QTabWidget(self.files_tab_widget_layout_widget)
        self.files_tab_widget.setStyleSheet(ss.files_tab_widget_stylesheet)
        self.files_tab_widget.setTabsClosable(True)
        self.files_tab_widget_layout.addWidget(self.files_tab_widget, 0, 0, 1, 1)
        self.files_tab_widget.tabCloseRequested.connect(self.closeTab)
        ###############
        ##OUTPUT TEXT##
        ###############
        self.files_path_dict={}
        self.output_plain_text_edit_layout_widget = QtWidgets.QWidget(self.input_output_splitter)
        self.output_plain_text_edit_layout = QtWidgets.QVBoxLayout(self.output_plain_text_edit_layout_widget)
        self.output_plain_text_edit_layout.setContentsMargins(0, 0, 0, 0)
        self.output_plain_text_edit_layout.setSpacing(0)
        self.output_plain_text_edit = QPlainTextEdit(self.output_plain_text_edit_layout_widget)
        self.output_plain_text_edit.setStyleSheet(ss.output_plain_text_edit_stylesheet)
        self.output_plain_text_edit_layout.addWidget(self.output_plain_text_edit)

        self.main_grid_layout.addWidget(self.title_bar_frame,0,0)
        self.main_grid_layout.addWidget(self.tool_bar_frame,1,0)
        self.main_grid_layout.addWidget(self.input_output_splitter,2,0)
        MainWindow.setCentralWidget(self.central_widget)
        main_window_size_grip = QtWidgets.QSizeGrip(MainWindow)
        main_window_size_grip.setStyleSheet("background-color: transparent;\n""border: 0px;\n")

    def openFile(self):
        self.file_dialog = QtWidgets.QFileDialog()
        self.file_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        self.file_dialog.setFilter(QtCore.QDir.Files)
        if self.file_dialog.exec_():
            file_name = self.file_dialog.selectedFiles()
            if file_name[0].endswith('.py'):
                with open(file_name[0], 'r') as f:
                    data = f.read()
                    self.newTab(data,file_name[0])
                    f.close()
            else:
                pass

    def saveFile(self):
        if self.files_tab_widget.currentIndex() == -1:
            pass
        else:
            if self.files_path_dict[self.files_tab_widget.currentIndex()] == "New File":
                self.saveFileAs()
            else:
                with open(self.files_path_dict[self.files_tab_widget.currentIndex()], 'w') as f:
                        data = self.files_tab_widget.currentWidget().toPlainText()
                        f.write(data)
                        f.close()

    def saveFileAs(self):
        if self.files_tab_widget.currentIndex() == -1:
            pass
        else:
            file_name = QtWidgets.QFileDialog.getSaveFileName(None, "Save file", "", ".py")
            if file_name[0] + file_name[1] == "":
                pass
            else:
                with open(file_name[0] + file_name[1], 'w') as f:
                        data = self.files_tab_widget.currentWidget().toPlainText()
                        f.write(data)
                        f.close()
                self.files_tab_widget.currentWidget().setPlainText(data)
                self.files_tab_widget.setTabText(self.files_tab_widget.currentIndex(),os.path.basename(file_name[0] + file_name[1]))
                self.files_path_dict[self.files_tab_widget.currentIndex()] = file_name[0] + file_name[1]

    def newTab(self,file_text="",file_path="New File"):
        self.tab_code_editor = QCodeEditor()
        self.tab_code_editor.setLineWrapMode(False)
        self.tab_code_editor.setStyleSheet(ss.tab_code_editor_stylesheet)
        self.tab_code_editor.setTabStopDistance(QtGui.QFontMetricsF(self.tab_code_editor.font()).horizontalAdvance(' ') * 4)
        self.tab_code_editor.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.tab_code_editor_highlighter = PythonHighlighter(self.tab_code_editor.document())
        tab_index = self.files_tab_widget.addTab(self.tab_code_editor,os.path.basename(file_path))
        self.input_output_splitter.setSizes([600,200])
        self.files_tab_widget.setCurrentIndex(tab_index)
        self.files_tab_widget.currentWidget().setPlainText(file_text)
        self.files_path_dict[self.files_tab_widget.currentIndex()]=file_path

    def closeTab(self,tab_index):
        self.files_tab_widget.removeTab(tab_index)
        self.files_path_dict.pop(tab_index)
        files_path_dict_values = list(self.files_path_dict.values())
        files_path_dict_keys = list(self.files_path_dict.keys())
        for index,item in enumerate(files_path_dict_keys):
            if item>tab_index:
                files_path_dict_keys[index]=item-1
        self.files_path_dict={}
        files_path_dict_values_iter = iter(files_path_dict_values)
        for x in files_path_dict_keys:
            self.files_path_dict[x] = next(files_path_dict_values_iter)

    def runCode(self):
        if self.files_tab_widget.currentIndex() == -1:
            pass
        else:
            self.output_plain_text_edit.clear()
            self.saveFile()
            command = 'python' + " \"" + self.files_path_dict[self.files_tab_widget.currentIndex()] + "\""
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()
            self.output_plain_text_edit.setPlainText(output.decode("utf-8") + error.decode("utf-8"))