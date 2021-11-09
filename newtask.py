#seperate module which contains the new task page to add new homework

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
# from kivymd.uix.dialog import MDInputDialog, MDDialog,BaseDialog
from kivy.properties import ObjectProperty, StringProperty
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.textfield import MDTextField

if __name__!='__main__':
    Builder.load_file('newtask.kv')

class SubjectDropDown(MDDropDownItem):
    #define the SubjectDropDown widget as an MD Drop Down menu
    pass

class SubjectTextField(MDTextField):
    #define the SubjectTextField widget as an MD text Field
    pass

class SubjectField(BoxLayout):
    #define the SubjectField as a Box Layou with a string property called 'text'
    text = StringProperty


class NewTaskPage(BoxLayout):
    #initiate variables for the page
    previous_date = None
    alert_dialog = None
    new_task_page = ObjectProperty(None)
    from datetime import date
    today = date.today()
    app = MDApp.get_running_app()


    def show_alert_dialog(self, alert_text):
        #create pop-up alert dialogue with text in parameter (used alognside data validation)
        if not self.alert_dialog:
            from kivymd.uix.dialog import MDDialog
            self.alert_dialog = MDDialog(
                title="Error",
                size_hint=(0.8, 0.4),
                text_button_ok="OK",
                text=alert_text,
            )
        self.alert_dialog.open()

    def check_data_task(self):
        #function to validate data, and save if everything is ok
        app = MDApp.get_running_app()

        #load field contents to variables
        task_name = self.ids.task_name.text
        task_type = self.ids.task_type_dropdown.current_item
        task_subject = self.ids.task_subject.text
        task_description = self.ids.task_description.text
        task_set = self.ids.date_set.text
        task_due = self.ids.date_due.text

        error_strings = []              #create list for errors
        if len(task_name) > 30:         #verify task name length
            error_string = 'Task Name must be 30 characters or less! Currently ' + str(len(task_name))
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        if len(task_subject) > 30:      #verify subject length
            error_string = 'Subject Name must be 30 characters or less! Currently ' + str(len(task_subject))
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        if len(task_description) > 500: #verify despcription length
            error_string = 'Description must be 500 characters or less! Currently ' + str(len(task_description))
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        if task_name == '':             #verify task name is entered
            error_string = 'Task Name missing! Must be entered.'
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        if task_subject == '':          #verify subject is entered
            error_string = 'Subject missing! Must be entered.'
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        
        if error_strings != []:         #check if there are any errors
            error_message =  '\n'.join(error_strings)   #Put all error messages into one string, seperated by newline
            self.show_alert_dialog(error_message)       #pop-up alert dialogue with error messages
        else:
            from lib import taskdb
            taskdb.InsertHW(app.dbPath, task_name, task_due, task_subject, task_set, task_type, task_description)
            #return_data()

            print('Name: ' + task_name)
            print('Type: ' + task_type)
            print('Subject: ' + task_subject)
            print('Description: ' + task_description)
            print('Date set: ' + task_set)
            print('Date due: ' + task_due)
            app.refeshTaskList()
            app.setSubjectList()
            app.refreshArchiveList()
            app.changeScreen('main_app_screen')

    def set_date_set(self, date_obj):
        self.ids.date_set.text = str(date_obj)

    def show_date_set_picker(self):
        from kivymd.uix.picker import MDDatePicker
        MDDatePicker(self.set_date_set).open()
    
    def set_date_due(self, date_obj):
        self.ids.date_due.text = str(date_obj)

    def show_date_due_picker(self):
        from kivymd.uix.picker import MDDatePicker
        MDDatePicker(self.set_date_due).open()
    
    def set_task_type_menu(self, item):
        self.ids.task_type_menu.text = item
    


    
if __name__=='__main__':
    class NewTaskApp(MDApp):
        title = 'Login Page Test'
        dbpath = 'homework.db'

        def build(self):
            return NewTaskPage()

    NewTaskApp().run()
