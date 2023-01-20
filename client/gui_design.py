import sys
import os 
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from api import database 

from auth import login

class LoginScreen(QMainWindow):
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
        if user_data['perm'] == 'member':
            self.memberHomeScreen()

        elif user_data['perm'] in ('hr', 'admin'):
            self.hrHomeScreen()

        self.stack = []
        self.logout_button.clicked.connect(self.logOut)   
        self.setUpAvatar()
        self.setUpResource()

    def memberHomeScreen(self):
        loadUi('GUI/home.ui', self)
        self.task_browser.setVisible(False)
        self.task_browser.setMouseTracking(True)
        self.task_browser.enterEvent = self.moveTaskBrowser

        self.calendar.clicked.connect(self.clickOnDate)

    def hrHomeScreen(self):
        loadUi('GUI/hr_home.ui', self)
        self.deadline_button.clicked.connect(self.goToDeadline)
        self.member_button.clicked.connect(self.goToMember)

    def setUpAvatar(self):
        self.name.setText(f"{user_data['name']}")
        self.title.setText(f"{user_data['title']}")
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

    def setUpResource(self):
        self.trello.clicked.connect(lambda: self.openLink('https://www.example.com'))
        self.drive.clicked.connect(lambda: self.openLink('https://www.example.com'))
        self.facebook.clicked.connect(lambda: self.openLink('https://www.example.com'))

    def openLink(self, url):
        url = QUrl(url)
        open_url = QDesktopServices.openUrl(url)
        if not open_url:
            QMessageBox.warning(self, 'Error', 'Unable to open link')
    
    def logOut(self):
        widget_stack.setCurrentIndex(0)
        widget_stack.removeWidget(widget_stack.widget(1))

    def goToDeadline(self):
        deadline_screen = ManageDeadlineScreen()
        widget_stack.addWidget(deadline_screen)
        widget_stack.setCurrentIndex(2) 

    def goToMember(self):
        member_screen = ManageMemberScreen()
        widget_stack.addWidget(member_screen)
        widget_stack.setCurrentIndex(2)

    def moveTaskBrowser(self, event):
        cursor = QCursor()
        pos = self.mapFromGlobal(cursor.pos())

        if pos.x() >= 440:
            self.task_browser.move(10, 320)
        else:
            self.task_browser.move(440, 320)

    def clickOnDate(self, date):
        print(f'Selected date: {date}')
        #database.load_deadline(date)

        # if date already in stack, means that this click is to exit 
        if date in self.stack: 
            self.stack = []
            self.task_browser.setVisible(False)
        # if date is not in stack, means this click is to open browser 
        else:
            self.stack.append(date)
            self.task_browser.setVisible(True)
        
        # load data to task browser 
        '''
        text = f'{database.task_name} - {database.deadline}\n Status: {database.status}\n' 
        self.task_browser.setPlainText(text)
        '''    

class ManageDeadlineScreen(QMainWindow):
    def __init__(self):
        super(ManageDeadlineScreen, self).__init__() 
        loadUi('GUI/hr_deadline.ui', self)
        self.goback_button.clicked.connect(self.goToHomeScreen)
        self.stack = []
        self.task_browser.setVisible(False)
        self.task_browser.setMouseTracking(True)
        self.task_browser.enterEvent = self.moveTaskBrowser
        
        self.calendar.clicked.connect(self.clickOnDate)
    
    def goToHomeScreen(self):
        widget_stack.setCurrentIndex(1)
        widget_stack.removeWidget(widget_stack.widget(2))
    
    def clickOnDate(self, date):
        print(f'Selected date: {date}')
        #database.load_deadline(date)

        # if date already in stack, means that this click is to exit 
        if date in self.stack: 
            self.stack = []
            self.task_browser.setVisible(False)
        # if date is not in stack, means this click is to open browser 
        else:
            self.stack.append(date)
            self.task_browser.setVisible(True)
        
        # load data to task browser 

        ''' For hr and admin
        text = f'{database.member_name} - {database.task_name} ({database.task_time})\n'
        self.task_browser.setPlainText(text)
        '''

    def moveTaskBrowser(self, event):
        cursor = QCursor()
        pos = self.mapFromGlobal(cursor.pos())

        if pos.x() >= 440:
            self.task_browser.move(10, 320)
        else:
            self.task_browser.move(440, 320)

class ManageMemberScreen(QMainWindow):
    def __init__(self):
        super(ManageMemberScreen, self).__init__() 
        loadUi('GUI/hr_member.ui', self)
        self.goback_button.clicked.connect(self.goToHomeScreen)

        self.search.returnPressed.connect(self.searchMember)

    def setUpMemberList(self):
        pass 

    def searchMember(self):
        name = self.search.text().strip()
        print(name)
        # display members as button in name_list 
        #
        #
        #

    def addMember(self):
        name = self.name_field_2.text().strip()
        title = self.title_field_2.text().strip()
        id = self.id_field_2.text().strip()
        dob = self.dob_field_2.text().strip()
        address = self.address_field_2.text().strip()

        # send data to database 
        #
        # post
        #

    def deleteMember(self):
        # delete
        pass 

    def updateMember(self):
        # put
        pass 

    def goToHomeScreen(self):
        widget_stack.setCurrentIndex(1)
        widget_stack.removeWidget(widget_stack.widget(2))

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




