import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from api import login, get_deadline_for_user


class LoginScreen(QMainWindow):
    def __init__(self, main_window):
        super(LoginScreen, self).__init__()
        loadUi('GUI/login.ui', self)

        self.setFixedSize(800, 800)

        self.main_window = main_window
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

        if not (len(email) and len(password)):
            print('You must fill in both fields')

        if login(email, password)['status'] == 'success':
            user_data = login(email, password)
            self.goToHomeScreen(user_data)
        else:
            print('Incorrect Email or Password')

    def goToHomeScreen(self, user_data):
        self.main_window.show_home_window(user_data)


class HomeScreen(QMainWindow):
    def __init__(self, main_window, user_data):
        super(HomeScreen, self).__init__()

        self.setFixedSize(800, 800)
        self.user_data = user_data
        if self.user_data['perm'] == 'member':
            self.memberHomeScreen()

        elif self.user_data['perm'] in ('hr', 'admin'):
            self.hrHomeScreen()

        self.stack = []
        self.main_window = main_window
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
        self.name.setText(f"{self.user_data['name']}")
        self.title.setText(f"{self.user_data['title']}")
        try:
            # path = get_avatar(user_data['id'])['path']
            path = ''
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
        self.trello.clicked.connect(
            lambda: self.openLink('https://trello.com/'))
        self.drive.clicked.connect(
            lambda: self.openLink('https://drive.google.com/drive/my-drive'))
        self.facebook.clicked.connect(
            lambda: self.openLink('https://www.facebook.com/KIPEVN'))

    def openLink(self, url):
        url = QUrl(url)
        open_url = QDesktopServices.openUrl(url)
        if not open_url:
            QMessageBox.warning(self, 'Error', 'Unable to open link')

    def logOut(self):
        self.main_window.go_back()

    def goToDeadline(self):
        self.main_window.show_deadline_window()

    def goToMember(self):
        self.main_window.show_member_window()

    def moveTaskBrowser(self, event):
        cursor = QCursor()
        pos = self.mapFromGlobal(cursor.pos())

        if pos.x() >= 440:
            self.task_browser.move(10, 320)
        else:
            self.task_browser.move(440, 320)

    def clickOnDate(self, date):
        print(f'Selected date: {date}')

        # if date already in stack, means that this click is to exit
        if date in self.stack:
            self.stack = []
            self.task_browser.setVisible(False)
        # if date is not in stack, means this click is to open browser
        else:
            self.stack.append(date)
            self.task_browser.setVisible(True)

        # convert date to mysql format
        deadline = date.toString('yyyy-MM-dd')

        # get task from database
        task_list = get_deadline_for_user(self.user_data['user_id'], deadline)
        print(task_list)

        # load data to task browser using this format
        # task_name - deadline
        # Status: status

        if not task_list:
            self.task_browser.setPlainText('No task available')
        
        else:
            task_content = ''
            num = 0
            for task in task_list:
                num += 1
                text = f'{task["task_name"]} - {deadline}\n Status: {task["status"]}\n'
                task_content += str(num) + '. ' + text
            
            self.task_browser.setPlainText(task_content)



if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget_stack = QStackedWidget()

    login_screen = LoginScreen()

    widget_stack.addWidget(login_screen)

    widget_stack.setFixedSize(800, 800)
    widget_stack.show()

    try:
        sys.exit(app.exec_())
    except:
        # delete all extra files created when running the program
        if os.path.exists('cache.json'):
            os.remove('cache.json')

        print('Exiting')
