from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QWidget, QTextBrowser, QTextEdit
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

import sys 

class EditableLabel(QFrame):
    def __init__(self, text, x, y, width, height, parent=None):
        super().__init__(parent)
        self.resize(width, height)
        # Create a label widget for displaying the text
        self.label = QLabel(text, self)
        self.label.setStyleSheet('''
            font: 75 20pt "MS Shell Dlg 2"; 
            color: rgb(246, 224, 181);    
        ''')
        self.label.resize(width, height)

        # Create a line edit widget for editing the label text
        self.line_edit = QLineEdit(self)
        self.line_edit.hide()
        self.line_edit.setStyleSheet('''
            border-radius: 15px;
            font-size: 20px;
            color: black;
        ''')
        self.line_edit.returnPressed.connect(self.update_label_text)
        
        self.line_edit.resize(width, height)
        # Create a layout for the label and line edit widgets
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        self.setLayout(layout)
        
        # Set the position of the QFrame
        self.move(x, y)
        
    def update_label_text(self):
        # Update the label text with the new value from the line edit widget
        new_text = self.line_edit.text()
        self.label.setText(new_text)
        self.label.show()
        self.line_edit.hide()
        
    def mouseDoubleClickEvent(self, event):
        # Show the line edit widget and hide the label widget when the QFrame is double-clicked
        self.label.hide()
        self.line_edit.setText(self.label.text())
        self.line_edit.show()
        self.line_edit.setFocus()
        self.line_edit.selectAll()

class EditableBrowser(QFrame):
    def __init__(self, text, x, y, width, height, parent=None):
        super().__init__(parent)
        self.resize(width, height)

        # Create a text browser widget for displaying the text
        self.browser = QTextBrowser(self)
        self.browser.setStyleSheet('''
            font: 75 20pt "MS Shell Dlg 2"; 
            color: rgb(246, 224, 181);
            background-color: transparent;         
            border: none;

        ''')
        self.browser.resize(width, height)
        self.browser.setText(text)
        self.browser.mousePressEvent = self.show_text_edit

        # Create a text edit widget for editing the label text
        self.text_edit = QTextEdit(self)
        self.text_edit.setStyleSheet('''
            border-radius: 15px;
            font-size: 20px;
            color: black;
        ''')
        self.text_edit.textChanged.connect(self.update_text)
        self.text_edit.resize(width, height)

        # Create a layout for the browser and text edit widgets
        layout = QHBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        
        # Set the position of the QFrame
        self.move(x, y)
        
        # Hide the text edit widget initially
        self.text_edit.hide()
        self.text_edit.setReadOnly(True)
        self.browser.show()
        
    def update_text(self):
        # Check if the Enter key was pressed
        if "\n" in self.text_edit.toPlainText():
            # Remove the Enter key from the text
            new_text = self.text_edit.toPlainText().replace("\n", "")
            # Update the label text with the new value from the line edit widget
            self.browser.setText(new_text)
            self.browser.show()
            self.text_edit.hide()
            self.text_edit.setReadOnly(True)
        
    def show_text_edit(self, event):
        # Hide the label widget and show the line edit widget when the QFrame is clicked
        self.browser.hide()
        self.text_edit.setReadOnly(False)
        self.text_edit.setText(self.browser.toPlainText())
        self.text_edit.show()
        self.text_edit.setFocus()
        self.text_edit.selectAll()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout()
    browser = EditableBrowser('This is a test text', 100, 100, 200, 200)
    layout.addWidget(browser)
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)
    window.show()
    sys.exit(app.exec_())