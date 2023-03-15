from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow

class EditableLabel(QFrame):
    def __init__(self, text, x, y, width, height, parent=None):
        super().__init__(parent)
        self.resize(width, height)
        # Create a label widget for displaying the text
        self.label = QLabel(text, self)
        self.label.setStyleSheet('''
            font: 75 20pt "MS Shell Dlg 2"; 
            color: rgb(246, 224, 181);
            text-align: right;         
        ''')
        self.label.resize(width, height)

        # Create a line edit widget for editing the label text
        self.line_edit = QLineEdit(self)
        self.line_edit.hide()
        self.line_edit.setStyleSheet('''
            border-radius: 20px;
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

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    window.resize(500, 500)
    # Create an EditableLabel widget with text "Hello", position (100, 100), and add it to the main window
    editable_label = EditableLabel("Hello", 300, 300, window)    
    window.show()
    app.exec_()