import sys
import os
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, Qt, QEvent
from api import get_user, create_user, update_user, delete_user, get_deadline, create_deadline, update_deadline, delete_deadline, login
from datetime import datetime
import functools


class LoginScreen(QMainWindow):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi('GUI/login.ui', self)

        self.setFixedSize(800, 800)

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
            global user_data
            user_data = login(email, password)
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

        self.setFixedSize(800, 800)
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
            # path = database.get_avatar(user_data['id'])['path']
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
            lambda: self.openLink('https://www.example.com'))
        self.drive.clicked.connect(
            lambda: self.openLink('https://www.example.com'))
        self.facebook.clicked.connect(
            lambda: self.openLink('https://www.example.com'))

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
        # database.load_deadline(date)

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

        self.date_selected = datetime.now().date() 

        self.setFixedSize(800, 800)
        self.goback_button.clicked.connect(self.goToHomeScreen)

        self.calendar.clicked.connect(self.loadDeadline)
        self.deadline_list.itemDoubleClicked.connect(self.updateDeadline)
        self.add_button.clicked.connect(self.addDeadline)
        
    def goToHomeScreen(self):
        widget_stack.setCurrentIndex(1)
        widget_stack.removeWidget(widget_stack.widget(2))
    
    def loadDeadline(self):
        self.deadline_list.clear()
        self.date_selected = self.calendar.selectedDate().toPyDate()
        tasks = get_deadline(self.date_selected)

        for task in tasks:
            if task['task_name'] == 'No deadlines found':
                item = QListWidgetItem(task['task_name'])
                self.deadline_list.addItem(item)
                continue

            if str(self.date_selected) + ' 00:00:00' == str(task['deadline']):
                item = QListWidgetItem(task['task_name'])
                self.deadline_list.addItem(item)

        ''' For hr and admin
        text = f'{database.member_name} - {database.task_name} ({database.task_time})\n'
        self.task_browser.setPlainText(text)
        '''
        pass 

    def addDeadline(self):
        self.goToAddDeadline()
        pass
    
    def updateDeadline(self):
        if self.deadline_list.currentItem():
            id = self.deadline_list.currentItem()
            name = self.name_field.text().strip()
            deadline = self.deadline
            status = self.status_field.text().strip()

            pass 

        # update_deadline(id, name, date, status)
        pass 

    def deleteDeadline(self):
        # select current item in the list
        if self.deadline_list.currentItem():
            id = self.deadline_list.currentItem()
            delete_deadline(id)

    def goToAddDeadline(self):
        add_deadline_screen = AddDeadlineDialog(self.date_selected)
        add_deadline_screen.exec_()

class AddDeadlineDialog(QDialog):
    def __init__(self, deadline):
        super(AddDeadlineDialog, self).__init__()
        loadUi('GUI/add_deadline.ui', self)
        self.setFixedSize(600, 600)
        self.deadline = deadline
        self.date_field.setText(str(self.deadline))
        self.add_button_2.clicked.connect(self.addDeadline)
    
    def addDeadline(self):
        id = user_data['user_id']
        name = self.name_field.text().strip()
        deadline = str(self.deadline) 
        description = self.description_field.toPlainText().strip()

        create_deadline(id, name, deadline, description)
        pass

class ManageMemberScreen(QMainWindow):
    def __init__(self):
        super(ManageMemberScreen, self).__init__()
        loadUi('GUI/hr_member.ui', self)

        self.setFixedSize(800, 800)
        self.name_list_container.setMaximumSize(300, 550)
        self.goback_button.clicked.connect(self.goToHomeScreen)
        self.search.returnPressed.connect(self.searchMember)
        self.address_field_2.returnPressed.connect(self.addMember)
        self.submit_button.clicked.connect(self.addMember)
        self.delete_button.clicked.connect(self.deleteMember)
        self.modify_button.clicked.connect(self.updateMember)

    def setUpMemberList(self, data):
        # delete all items from list
        for i in reversed(range(self.name_list.count())):
            self.name_list.itemAt(i).widget().setParent(None)

        # display members as button in name_list
        if data:
            for item in data:
                name = f"{item['user_id']} - {item['name']}"
                button = QPushButton(name)
                button.clicked.connect(functools.partial(
                    self.parseMemberToModifyForm, item))

                stylesheet = '''
                    border-radius: 20px;
                    background-color: rgb(246, 224, 181);
                    font: 75 18pt "MS Shell Dlg 2";
                '''

                button.setStyleSheet(stylesheet)
                self.name_list.addWidget(button)
        else:
            stylesheet = '''
                font: 75 20pt "MS Shell Dlg 2"; 
                color: rgb(246, 224, 181);
            '''
            label = QLabel('No member found')
            label.setStyleSheet(stylesheet)
            label.setAlignment(Qt.AlignCenter)
            self.name_list.addWidget(label)

    def parseMemberToModifyForm(self, item):
        # Modify dob format
        dob_str = datetime.strptime(
            item['dob'], '%Y-%m-%d').strftime('%d/%m/%Y')

        # set texts of Mofidy Form
        self.name_field.setText(item['name'])
        self.title_field.setText(item['title'])
        self.id_field.setText(str(item['user_id']))
        self.dob_field.setText(dob_str)
        self.address_field.setText(item['address'])

    def searchMember(self):
        name = self.search.text().strip()
        data = get_user(name)

        self.setUpMemberList(data)

    def addMember(self):
        name = self.name_field_2.text().strip()
        title = self.title_field_2.text().strip()
        dob = self.dob_field_2.text().strip()
        address = self.address_field_2.text().strip()

        #reformat dob
        dob = datetime.strptime(dob, "%d/%m/%Y").strftime("%Y-%m-%d")

        # send data to database
        create_user(name, title, 'member', dob, address)

    def deleteMember(self):
        # delete
        id = int(self.id_field.text().strip())
        delete_user(id)

    def updateMember(self):
        # put
        id = self.id_field.text().strip()
        name = self.name_field_2.text().strip()
        title = self.title_field_2.text().strip()
        dob = self.dob_field_2.text().strip()
        address = self.address_field_2.text().strip()
        update_user(id, name, title, 'member', dob, address)

    def goToHomeScreen(self):
        widget_stack.setCurrentIndex(1)
        widget_stack.removeWidget(widget_stack.widget(2))

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
