from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
# from kivymd.uix.dialog import MDInputDialog, MDDialog,BaseDialog
from kivy.properties import ObjectProperty, StringProperty
from kivy.storage.jsonstore import JsonStore

if __name__!='__main__':
    Builder.load_file('settings.kv')

class SettingsPage(GridLayout):
    
    def set_home_times(self):
        #changes current stop to home
        app = MDApp.get_running_app()
        app.currentStop = 'home'
        self.exit_settings()
    
    def set_school_times(self):
        #changes current stop to school
        app = MDApp.get_running_app()
        app.currentStop = 'school'
        self.exit_settings()
    
    def save_settings(self):
        #updates global variables with current settings
        app = MDApp.get_running_app()
        app.home_stop = self.ids.home_stop.text
        app.school_stop = self.ids.school_stop.text
        app.archive = self.ids.archive_switch.active
        app.store_settings()    #save settings to JSON file
        self.exit_settings()

    def exit_settings(self):
        #refresh all data to reflect changes to settings, then leave settings screen
        app = MDApp.get_running_app()
        app.refresh_all()
        app.changeScreen('main_app_screen')

    
if __name__=='__main__':
    class SettingsApp(MDApp):
        home_stop = ''
        school_stop = '036006209209'
        title = 'Settings Test'
        currentStop = 'school'
        
        archive = True
        
        def refreshBusTimes(self):
            print(self.currentStop)
        
        def refresh_all(self):
            print('refresh')
            print('home stop: ' + self. home_stop)
            print('school stop: ' + self.school_stop)
            print('current stop: ' + self.currentStop)
            print('auto-archive: ' + str(self.archive))

        def changeScreen(self, new_Screen):
            print('Change screen to ' + new_Screen)

        def store_settings(self):
            app = self
            store = JsonStore('settings.json')
            store['settings'] = {
                'home_stop': app.home_stop,
                'school_stop': app.school_stop,
                'archive': app.archive
            }
        
        def load_settings(self):
            app = self
            store = JsonStore('settings.json')
            if store.exists('settings'):
                app.home_stop = store['settings']['home_stop']
                app.school_stop = store['settings']['school_stop']
                app.archive = store['settings']['archive']


        
        def build(self):
            self.load_settings()
            return SettingsPage()
            

    SettingsApp().run()
    