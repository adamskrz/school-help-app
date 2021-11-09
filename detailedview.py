from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
# from kivymd.uix.dialog import MDInputDialog, MDDialog,BaseDialog
from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from lib.taskdb import DeleteHW

if __name__!='__main__':
    #if module is being run from a different porgram, load the kv code for it
    Builder.load_file('detailedview.kv')

class DetailedViewPage(BoxLayout):
    #initiate variables for the page
    previous_date = None
    alert_dialog = None
    ok_cancel_dialog = None
    new_task_page = ObjectProperty(None)
    from datetime import date
    today = date.today()
    app = MDApp.get_running_app()
    widgets_disabled = BooleanProperty(True)

    def load_data(self):
        #function to fill the data fields with the selected task
        from lib.taskdb import DetailedInfo
        app = MDApp.get_running_app()
        task = app.current_hwid

        #get the data from the database for the chosen task id
        task_data = DetailedInfo(app.dbPath, task)
        print(task_data)

        #fill the fields with the data fetched
        self.ids.task_name.text = task_data['taskName']
        self.ids.task_type_dropdown.set_item(task_data['taskType'])
        self.ids.task_subject.text = task_data['subject']
        self.ids.task_description.text = task_data['description']
        self.ids.date_set.text = task_data['issueDate']
        self.ids.date_due.text = task_data['dueDate']
        self.ids.task_done.active = task_data['done']

    def update_widgets(self):
        #function update each widget with enablement status
        for widget in [
            self.ids.task_name,
            self.ids.task_type_dropdown,
            self.ids.task_subject,
            self.ids.task_description,
            self.ids.date_set,
            self.ids.date_due,
            self.ids.task_done
        ]:
            widget.disabled = self.widgets_disabled
        
        if self.widgets_disabled:
            self.ids.cancel_button.text = 'Close'
            self.ids.action_button.text = 'Edit'
        else:
            self.ids.cancel_button.text = 'Cancel'
            self.ids.action_button.text = 'Save'
        
    def action_callback(self):
        #callback for edit/save button
        print('press')
        if self.widgets_disabled == True:
            self.widgets_disabled = False
            self.update_widgets()
        else: 
            self.check_data_task()

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
    
    def show_delete_dialog(self):
        #create a pop-up dialogue to confirm deletion of a homework item
        task_name = self.ids.task_name.text
        if not self.ok_cancel_dialog:
            from kivymd.uix.dialog import MDDialog
            message = "Are you sure you want to delete " + task_name + '?\nThis is irreversible!'
            self.ok_cancel_dialog = MDDialog(
                title="Delete",
                size_hint=(0.8, 0.4),
                text_button_ok="Delete",
                text=message,
                text_button_cancel="Cancel",
                events_callback=self.delete_dialog_callback,
            )
        self.ok_cancel_dialog.open()
    
    def delete_dialog_callback(self, *args):
        #callback for the delete dialogue confirm button
        app = MDApp.get_running_app()
        if args[0] == 'Delete':
            DeleteHW(app.dbPath, app.current_hwid)  #delete the task from the database
            app.refeshTaskList()
            app.refreshArchiveList()                #refresh all the homework pages to reflect changes
            self.exit_screen()                      #exit the screen

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
        task_complete = self.ids.task_done.active
        error_strings = []              #create list for errors

        if len(task_name) > 30:         #verify task name length
            error_string = 'Task Name must be 30 characters or less! Currently ' + str(len(task_name))
            error_strings.append(error_string)  #if verification failed, add the error message to existing list
        if len(task_subject) > 20:      #verify subject length
            error_string = 'Subject Name must be 20 characters or less! Currently ' + str(len(task_subject))
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
        
        else:       #if there are any errors, save the new data
            from lib import taskdb
            #load new data to the database
            taskdb.UpdateHW(app.dbPath, app.current_hwid, task_name, task_due, task_subject, task_complete, task_set, task_type, task_description)
            
            # print('Name: ' + task_name)
            # print('Type: ' + task_type)
            # print('Subject: ' + task_subject)
            # print('Description: ' + task_description)
            # print('Date set: ' + task_set)
            # print('Date due: ' + task_due)
            # print('Task done? ' + str(task_complete))

            app.refeshTaskList()        #refresh lists of homework
            app.refreshArchiveList()
            self.exit_screen()          #leave the detailed homework screen
    

    def exit_screen(self):
        #when leaving edit screen, restore widget status to non-editable
        self.widgets_disabled = True
        self.update_widgets()
        #switch screen back to main
        MDApp.get_running_app().changeScreen('main_app_screen')


    def set_date_set(self, date_obj):
        #callback to set label text when new date picked
        self.ids.date_set.text = str(date_obj)

    def show_date_set_picker(self):
        #open up the date picker when the field is selected
        from kivymd.uix.picker import MDDatePicker
        MDDatePicker(self.set_date_set).open()
    
    def set_date_due(self, date_obj):
        self.ids.date_due.text = str(date_obj)

    def show_date_due_picker(self):
        from kivymd.uix.picker import MDDatePicker
        MDDatePicker(self.set_date_due).open()


    
if __name__=='__main__':
    #data for testing module individually

    class DetailedViewApp(MDApp):
        title = 'Login Page Test'
        dbPath = 'homework.db'
        current_hwid = NumericProperty(1)

        def build(self):
            return DetailedViewPage()

        def on_start(self):
            MDApp.get_running_app().root.load_data()
        
        def refreshArchiveList(self):
            print('refresh archive')
        
        def refeshTaskList(self):
            print('refresh tasks')
        
        def changeScreen(self,screen):
            print('Changing screen to ' + screen)

        

    DetailedViewApp().run()
