import sys
import os 
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from api import database 

from auth import hash_password, compare_hashes, login

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('GUI/login.ui', self) 

        self.email.setMaxLength(45)
        self.email.returnPressed.connect(self.password.setFocus)

        self.password.setMaxLength(45)
        self.password.setEchoMode(QLineEdit.Password)
        self.password.returnPressed.connect(self.logIn)

        self.login_button.clicked.connect(self.logIn)
    
    def logIn(self):
        # get email from input
        email = self.email.text().strip()
        password = self.password.text().strip()
    
        if login(email, password)[0]:
            global user_data
            user_data = login(email, password)[1]
            self.goToHomeScreen()
        else:
            print('Incorrect Email or Password')

    def goToHomeScreen(self):
        home_screen = HomeScreen()
        widget_stack.addWidget(home_screen)
        widget_stack.setCurrentIndex(1)

class HomeScreen(QMainWindow):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi('./GUI/home.ui', self)

        self.logout_button.clicked.connect(self.logOut)   
        self.setUpAvatar()

    def setUpAvatar(self):
        self.name.setText(f"{user_data['first_name']} {user_data['last_name']}")
        try: 
            path = database.get_avatar(user_data['id'])['path']
            
            if not os.path.isfile(path): 
                raise FileNotFoundError

        except Exception:
            # default image
            path = './Resource/default_avatar.png'
            print('Unable to set up avatar')

        pixmap = QPixmap(path)
        avatar = QIcon(pixmap)
        
        self.avatar.setIcon(avatar)

    def logOut(self):
        widget_stack.setCurrentIndex(0)
        widget_stack.removeWidget(widget_stack.widget(1))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget_stack = QStackedWidget()

    login_screen = LoginScreen()

    widget_stack.addWidget(login_screen)

    widget_stack.setFixedHeight(800)
    widget_stack.setFixedWidth(800)
    widget_stack.show()

    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')




