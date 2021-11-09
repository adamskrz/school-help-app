from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivymd.uix.list import TwoLineAvatarListItem, TwoLineListItem, OneLineAvatarListItem
from kivymd.uix.tab import MDTabsBase
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.storage.jsonstore import JsonStore
import os.path

from lib.bus.data import AllBusData
from StopInfo import StopInfo
from lib import taskdb
from newtask import NewTaskPage
from settings import SettingsPage
from detailedview import DetailedViewPage

class ContentScroll(ScrollView):
    #define the ContentScroll widget as a ScrollView
    pass

class ContentHomeworkScroll(BoxLayout):
    #define the ContentHomeworkScroll widget as a BoxLayout
    pass

class ContentHwView(BoxLayout):
    #define the ContentHwView page as a BoxLayout
    pass

class HomeworkListItem(TwoLineListItem):
    #define HomeworkListItem as a TwoLineListItem but with the extra attribute 'task_id'
    task_id = NumericProperty()

class HomeworkGridItem(BoxLayout):
    #define HomeworkListItem as a BoxLayout with the extra attributes name, subject, and due date
    name = StringProperty()
    subject = StringProperty()
    due = StringProperty()


class DetailedBusItem(TwoLineAvatarListItem):
    #define HomeworkListItem as a TwoLineListItem with an icon at the extra attribute 'icon'
    icon = StringProperty()

class ShortBusItem(OneLineAvatarListItem):
    #define HomeworkListItem as a OneLineListItem with an icon at the extra attribute 'icon'
    icon = StringProperty()

class HomeworkTab(BoxLayout, MDTabsBase):
    #define the tabs on the homework page as BoxLayouts
    pass


class SchoolApp(MDApp):
    #instantiate basic settings and global variables
    dbPath = StringProperty('homework.db')
    sub_list = ListProperty()
    home_stop = StringProperty('036006209209')
    school_stop = StringProperty('03700075')
    currentStop = StringProperty('school')
    bus_title = StringProperty('Bus times')
    current_hwid = NumericProperty()
    archive = BooleanProperty(False)

    def build(self):
        #the build function is the first thing that is run, telling the program to load settings from file and then the main GUI file
        self.load_settings()
        return Builder.load_file('main.kv')

    def load_settings(self):
        #if the settings file exists, load the school and home stops, and the automatic archiving setting
        app = self.get_running_app()
        store = JsonStore('settings.json')
        if store.exists('settings'):
            app.home_stop = store['settings']['home_stop']
            app.school_stop = store['settings']['school_stop']
            app.archive = store['settings']['archive']
    


    def on_start(self):
        #once the GUI is created, the following code is run
        
        #setting the current stop to school, if it is the afternoon
        import datetime
        dt = datetime.datetime.now()
        if dt.time() < datetime.time(12, 30):
            self.currentStop = 'home'

        if not self.previously_open_check():
            #if the app has not been set-up previously
            #open the settings screen
            self.changeScreen('settings_screen')
        
        #refresh all loads all the data
        self.refresh_all()

        #schedules the bus times to be refreshed in 30 seconds
        Clock.schedule_once(self.bus_auto_refresh, 30)

    def previously_open_check(self):
        #checks for the existence of settings file
        if os.path.isfile('settings.json'):
            #if settings exist, return true
            print('settings detected')
            return True
        else:
            #otherwise, return false
            print('no settings detected')
            return False

    def refresh_all(self):
        self.refreshBusTimes()      #load bus times
        self.refeshTaskList()       #load current homework tasks
        self.setSubjectList()       #load list of subjects from the database
        self.refreshArchiveList()   #load list of all tasks for selected subject
    
    def bus_auto_refresh(self, now = True):
        #function to automatically refresh bus times every 30 seconds
        if now:
            if self.root.ids.panel.ids.tab_manager.current in ['bus','home']:
                #if the app currently has a tab containing bus times open, refresh the bus times, and schedule another refresh in 30 seconds
                self.refreshBusTimes()
                Clock.schedule_once(self.bus_auto_refresh, 30)
            else:
                #if any other part of the app is open, just schedule it to check again in 30 seconds
                Clock.schedule_once(self.bus_auto_refresh, 30)
        else:
            #provides a method to schedule another refresh without actually refresshing on the call
            Clock.schedule_once(self.bus_auto_refresh, 30)

    def setBusList(self):
        #function to set the lists of bus times

        #sets the current bus stop code to request data for to match the current stop variable
        if self.currentStop == 'school':
            current_atco = self.school_stop
        elif self.currentStop == 'home':
            current_atco = self.home_stop
        
        #sets the title of the bus times tab to reflect the times shown
        self.bus_title = 'Bus times for ' + self.currentStop
        
        #gets all the bus times from the bus time module
        results = AllBusData(current_atco)

        for bus in results:
            #iterating though each bus in order to add the time to the lists

            #calculating the time until the bus
            min, sec = divmod((bus['departure']-bus['requestTime']).total_seconds(),60)
            text = str(int(min)) + " mins " + str(int(sec)) + " seconds"

            #creating text for the departure list, based on whether the time is live or not
            if bus['live']:
                secondary_text = bus['destination'] + ', Live: ' + bus['departure'].astimezone(tz=None).strftime("%H:%M:%S") + ', Operator: ' + bus['operator']
            else: 
                secondary_text = bus['destination'] + ', Scheduled: ' + bus['departure'].astimezone(tz=None).strftime("%H:%M:%S") + ', Operator: ' + bus['operator']
            icon = 'img/' + str(bus['line']) + '.png'
            
            #adding full bus details to the bus times page
            self.root.ids.bus_scroll.ids.box_item.add_widget(
                DetailedBusItem(
                    text=text,
                    icon=icon,
                    secondary_text= secondary_text,
                )
            )

            #adding short bus details to the home page
            self.root.ids.short_bus.ids.box_item.add_widget(
                ShortBusItem(
                    text=text, #the text is the minutes and seconds left
                    icon=icon, #the icon is the bus number in its colour
                )
            )
        
        #adding extra data information to the bottom of the bus times
        refreshText = 'Last refresh: ' + str(results[0]['requestTime'].astimezone(tz=None).strftime("%H:%M:%S"))
        self.root.ids.bus_scroll.ids.box_item.add_widget(
            DetailedBusItem(
                text= refreshText,
                secondary_text='Data provided by: TfL, Traveline, Reading Buses',
                icon= 'img/refresh.png',
            )
        )
        
    def refreshBusTimes(self):
        #function used when refreshing bus times - clears both bus tile lists, then reloads them
        self.root.ids.bus_scroll.ids.box_item.clear_widgets()
        self.root.ids.short_bus.ids.box_item.clear_widgets()
        self.setBusList()
    
    def setTaskList(self):
        #function to load the list of current homework tasks

        taskdb.checkDB(self.dbPath)                 #check if the homework database exists, or create a new one
        tasks = taskdb.CurrentTasks(self.dbPath)    #load all the current tasks from the database
        tasks.sort(key=lambda x:x['dueDate'])       #sort tasks, earliest due date first
        
        for task in tasks:
            if self.archive:
                #if auto-archival is on in settings, archive task if was due before today
                import datetime
                today = datetime.date.today()
                if str(today) > task['dueDate']:
                    taskdb.SetArchiveHW(self.dbPath, task['taskID'], True)
                    continue
            
            #add the task to the main homework list
            text = task['taskName'] + ', ' + task['subject'] 
            secondarytext = task['dueDate'] + ' ' + str(task['taskID'])
            self.root.ids.homework_screen.ids.current_task_scroll.ids.box_item.add_widget(
                HomeworkListItem(
                    text=text,
                    secondary_text= secondarytext,
                    task_id = task['taskID']
                )
            )

            #add the task to the home page list
            self.root.ids.short_hw.ids.box_item.add_widget(
                HomeworkGridItem(
                    name = task['taskName'],
                    subject = task['subject'],
                    due = task['dueDate']
                )
            )

    def setSubjectList(self):
        #function to load every subject to a list
        self.sub_list = taskdb.SubjectList(self.dbPath)

    def setArchiveList(self):
        #function to load list of all homework for a specific subject
        self.sub_list = taskdb.SubjectList(self.dbPath)                                     #refresh list of subjects
        subject = self.root.ids.homework_screen.ids.subject_dropdown.current_item           #get the currently selected subject name
        tasks = taskdb.ArchiveTasks(self.dbPath,subject)                                    #retreive tasks for selected subject
        for task in tasks:
            #add each task to the archive list
            text = task['taskName'] + ', Set on ' + task['issueDate']
            secondarytext = 'Due: ' + task['dueDate'] + ' ' + str(task['taskID'])
            self.root.ids.homework_screen.ids.subject_task_scroll.ids.box_item.add_widget(
                HomeworkListItem(
                    text=text,
                    secondary_text= secondarytext,
                    task_id = task['taskID']
                )
            )

    def refreshArchiveList(self):
        #function to clear out the archive list of tasks, then reload it
        self.root.ids.homework_screen.ids.subject_task_scroll.ids.box_item.clear_widgets()
        self.setArchiveList()

    def refeshTaskList(self):
        #function to clear out the current list of tasks, then reload it
        self.root.ids.homework_screen.ids.current_task_scroll.ids.box_item.clear_widgets()
        self.root.ids.short_hw.ids.box_item.clear_widgets()
        self.setTaskList()

    def changeScreen(self, screen):
        #function to change the app screen to the desired one instantly
        print(screen)
        sm = self.root
        sm.transition = NoTransition()
        sm.current = screen
    
    def store_settings(self):
        #function to store the current settings to an external JSON file
        app = self.get_running_app()
        store = JsonStore('settings.json')
        store['settings'] = {
            'home_stop': app.home_stop,
            'school_stop': app.school_stop,
            'archive': app.archive
        }
    
    def homework_detailed_view(self, id):
        #function to open the detailed view page for a specific task
        self.current_hwid = id
        self.changeScreen('detailed_view_screen')
        self.root.ids.detailed_view.load_data()

SchoolApp().run()