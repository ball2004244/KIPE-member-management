from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout

class EditableLabel(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.label = QLabel('Click to edit')
        self.edit = QLineEdit()
        self.edit.hide()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.edit)

        self.label.mousePressEvent = self.label_clicked
        self.edit.editingFinished.connect(self.edit_finished)

        self.setLayout(self.layout)

    def label_clicked(self, event):
        self.label.hide()
        self.edit.show()
        self.edit.setFocus()

    def edit_finished(self):
        self.label.setText(self.edit.text())
        self.label.show()
        self.edit.hide()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = EditableLabel()
    w.show()
    sys.exit(app.exec_())
    