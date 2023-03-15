from PyQt5.QtWidgets import QMainWindow, QDialog, QListWidgetItem, QPushButton, QLabel
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from datetime import datetime
from api import get_user, create_user, update_user, delete_user, get_deadline, create_deadline, update_deadline, delete_deadline, login
from component import EditableLabel, EditableBrowser
import functools

class ManageDeadlineScreen(QMainWindow):
    def __init__(self, main_window):
        super(ManageDeadlineScreen, self).__init__()
        loadUi('GUI/hr_deadline.ui', self)
        self.deadline_data = {}
        self.main_window = main_window

        self.date_selected = datetime.now().date() 
        self.loadDeadline()
        self.setFixedSize(800, 800)
        self.goback_button.clicked.connect(self.goToHomeScreen)

        self.calendar.clicked.connect(self.loadDeadline)
        self.deadline_list.itemDoubleClicked.connect(self.goToModifyDeadline)
        self.add_button.clicked.connect(self.goToAddDeadline)
        
    def goToHomeScreen(self):
        self.main_window.go_back()
    
    def goToAddDeadline(self):
        add_deadline_screen = AddDeadlineDialog(self.date_selected)
        add_deadline_screen.exec_()

    def goToModifyDeadline(self):
        try:
            item = self.deadline_list.currentItem()
            task_id = item.text().split(' - ')[0]
            data = self.deadline_data[int(task_id)]
            modify_deadline_screen = ModifyDeadlineDialog(data)
            modify_deadline_screen.exec_()
        except Exception as e:
            print('Deadline does not exist')
            print(e)

    def loadDeadline(self):
        self.deadline_list.clear()
        self.date_selected = self.calendar.selectedDate().toPyDate()
        tasks = get_deadline(str(self.date_selected))

        for task in tasks:
            if str(self.date_selected) == str(task['deadline']):
                label = str(task['task_id']) + ' - ' + task['task_name']
                item = QListWidgetItem(label)
                self.deadline_list.addItem(item)
                self.deadline_data[task['task_id']] = task

        pass 

class AddDeadlineDialog(QDialog):
    def __init__(self, deadline):
        super(AddDeadlineDialog, self).__init__()
        loadUi('GUI/add_deadline.ui', self)

        self.setFixedSize(600, 600)
        self.deadline = deadline
        self.date_field.setText(str(self.deadline))
        self.add_button.clicked.connect(self.addDeadline)
    
    def addDeadline(self):
        try:
            id = self.assigned_field.text().strip()
            name = self.name_field.text().strip()
            deadline = str(self.deadline) 
            description = self.description_field.toPlainText().strip()
            if not name:
                print('Name cannot be empty')
                return
            
            create_deadline(id, name, deadline, description)
            get_deadline(str(deadline))
            print('Successfully add deadline')
        except Exception as e:
            print('Cannot add deadline')
            print(e)
        
        pass

class ModifyDeadlineDialog(QDialog):
    def __init__(self, data):
        super(ModifyDeadlineDialog, self).__init__()
        loadUi('GUI/modify_deadline.ui', self)
        self.setFixedSize(600, 600)

        self.data = data

        self.name_field = EditableLabel(str(self.data.get('task_name', '')), 200, 90, 350, 40, self)
        self.modify_id_field = EditableLabel(str(self.data.get('user_id', '')), 200, 160, 350, 40, self)
        self.deadline_field = EditableLabel(str(self.data.get('deadline', '')), 200, 230, 350, 40, self)
        self.status_field = EditableLabel(str(self.data.get('status', '')), 200, 300, 350, 40, self)
        self.description_field = EditableBrowser(str(self.data.get('description', '')), 200, 370, 350, 120, self)

        self.modify_button.setFocusPolicy(Qt.NoFocus)
        self.delete_button.setFocusPolicy(Qt.NoFocus)
        self.modify_button.clicked.connect(self.updateDeadline)
        self.delete_button.clicked.connect(self.deleteDeadline)

    def updateDeadline(self):
        try:
            task_id = int(self.data['task_id'])
            uid = int(self.modify_id_field.label.text().strip())
            name = self.name_field.label.text().strip()
            deadline = self.deadline_field.label.text().strip()
            status = self.status_field.label.text().strip()
            description = self.description_field.browser.toPlainText().strip()
            update_deadline(task_id, uid, name, deadline, status, description)
            print('Successfully update deadline')
        
        except Exception as e:
            print('Cannot update deadline')
            print(e)        
        pass 

    def deleteDeadline(self):
        try: 
            id = self.data['task_id']
            delete_deadline(id)
            print('Successfully delete deadline')
        except Exception as e:
            print('Cannot delete deadline')
            print(e)
        pass

class ManageMemberScreen(QMainWindow):
    def __init__(self, main_window):
        super(ManageMemberScreen, self).__init__()
        loadUi('GUI/hr_member.ui', self)

        self.main_window = main_window

        self.setFixedSize(800, 800)

        self.modify_name_field = EditableLabel('', 530, 200, 250, 40, self)
        self.modify_title_field = EditableLabel('', 530, 240, 250, 40, self)
        self.modify_dob_field = EditableLabel('', 530, 320, 250, 40, self)
        self.modify_address_field = EditableLabel('', 530, 360, 250, 40, self)
        
        self.name_list_container.setMaximumSize(300, 550)
        self.goback_button.clicked.connect(self.goToHomeScreen)
        self.search.returnPressed.connect(self.searchMember)

        self.address_field.returnPressed.connect(self.addMember)
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

        # set texts of Mofidy Form
        self.modify_name_field.label.setText(item['name'])
        self.modify_title_field.label.setText(item['title'])
        self.modify_id_field.setText(str(item['user_id']))
        self.modify_dob_field.label.setText(item['dob'])
        self.modify_address_field.label.setText(item['address'])

    def searchMember(self):
        name = self.search.text().strip()
        data = get_user(name)

        self.setUpMemberList(data)
        self.search.setText('')

    def addMember(self):
        name = self.name_field.text().strip()
        title = self.title_field.text().strip()
        dob = self.dob_field.text().strip()
        address = self.address_field.text().strip()

        create_user(name, title, 'member', dob, address)

        # clear all fields
        self.name_field.setText('')
        self.title_field.setText('')
        self.dob_field.setText('')
        self.address_field.setText('')
        
    def deleteMember(self):
        id = int(self.modify_id_field.text().strip())
        delete_user(id)

    def updateMember(self):
        id = self.modify_id_field.text().strip()
        name = self.modify_name_field.label.text().strip()
        title = self.modify_title_field.label.text().strip()
        dob = self.modify_dob_field.label.text().strip()
        address = self.modify_address_field.label.text().strip()

        update_user(id, name, title, 'member', dob, address)

    def goToHomeScreen(self):
        self.main_window.go_back()