from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
import sys, os
from general_screen import LoginScreen, HomeScreen
from hr_screen import ManageDeadlineScreen, ManageMemberScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KIPE Management System')
        self.widget_stack = QStackedWidget()

        login_window = LoginScreen(self)
        self.widget_stack.addWidget(login_window)
        
        self.widget_stack.setCurrentIndex(0)
        self.setCentralWidget(self.widget_stack)

    def show_home_window(self, user_data):
        home_window = HomeScreen(self, user_data)
        self.widget_stack.addWidget(home_window)
        self.widget_stack.setCurrentIndex(1)

    def show_deadline_window(self):
        deadline_window = ManageDeadlineScreen(self)
        self.widget_stack.addWidget(deadline_window)
        self.widget_stack.setCurrentIndex(2)
    
    def show_member_window(self):
        member_window = ManageMemberScreen(self)
        self.widget_stack.addWidget(member_window)
        self.widget_stack.setCurrentIndex(2)


    def go_back(self):
        current_index = self.widget_stack.currentIndex()
        try: 
            self.widget_stack.setCurrentIndex(current_index - 1)
            self.widget_stack.removeWidget(self.widget_stack.widget(current_index))
        except:
            print('Cannot go back')


# Create the application and main window
app = QApplication(sys.argv)
main_window = MainWindow()

# Set the size of the main window
main_window.setFixedSize(800, 800)

# Show the main window
main_window.show()

# Run the application
sys.exit(app.exec_())

