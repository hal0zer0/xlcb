# -*- coding: utf-8 -*-
from xl.nls import gettext as _
from xl import settings as xlsettings
from xl import event

import pygtk
import gtk
import gtk.glade
import os

###############################################
### Base functions for pluginability
def enable(exaile):
    if (exaile.loading):
        event.add_callback(_enable, 'exaile_loaded')
    else:
        _enable(None, exaile, None)
 
def disable(exaile):
    print('I am being disabled.')
 
def _enable(eventname, exaile, nothing):
    print('You enabled me!')
    plugin = xlcb(exaile)
    
    
###############################################
### Actual plugin code
class xlcb:
  
  def __init__(self, exaile):
    self.pluginName = "XLCB"
    # Add XLCB item to Tools menu
    self.MENU_ITEM = gtk.MenuItem(_('XLCB'))
    self.MENU_ITEM.connect('activate', self.show_gui, exaile)
    exaile.gui.builder.get_object('tools_menu').append(self.MENU_ITEM)
    self.MENU_ITEM.show()


  def show_gui(self, something, exaile):
    #Find and display GUI
    #ui_info = (os.path.dirname(__file__) + "/xlcbgui.glade", 'NameOfRootElement')
    self.gladefile = os.path.dirname(__file__) + "/xlcbgui.glade"
       
    self.builder = gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    
    buttonActions = { "on_beginButton_clicked" : self.startBuilding,
            "on_MainWindow_destroy" : gtk.main_quit }
            #"on_MainWindow_destroy" : self.testfunc }
    self.builder.connect_signals(buttonActions)
    
    self.window = self.builder.get_object("window1")
    self.populate()
    self.window.show_all()
    gtk.main()

  def startBuilding(self, arg):
    print "BOOBS!"
    print type(arg)
    self.saveSettings()
  
  
  def populate(self):
    settingsDict = self.getSettings()
    self.builder.get_object("albumNameEntry").set_text(settingsDict["albumName"])
    self.builder.get_object("albumInFileNameCheckbox").set_active(settingsDict["albumInFileName"])

    
  def getSettings(self):

    #                  Name of setting: default value
    self.defaultSettings = {"albumName":      "XLCB Comp",
                "albumInFileName":False,
                "authorName":     "Unknown",
                "outputDir":      os.path.expanduser('~'),
                "smartNaming":    True}
    print "DEFAULTS:", self.defaultSettings
    
    # Use Exaile's settings if there, defaults if not
    pluginSettings = {}
    for settingName in self.defaultSettings:
      optionPath = "/".join(("plugin", self.pluginName, settingName))
      print optionPath
      pluginSettings[settingName] = xlsettings.get_option(optionPath, self.defaultSettings[settingName])
      
    print "EXAILE:", pluginSettings
    return pluginSettings
    
  def saveSettings(self):
    toSave = [["albumName", self.builder.get_object("albumNameEntry").get_text()],
              ["albumInFileName",  self.builder.get_object("albumInFileNameCheckbox").get_active()]]
    for setting in toSave:
      optionPath = "/".join(("plugin", self.pluginName, setting[0]))
      xlsettings.set_option(optionPath, setting[1])

      
    
    
    
    
    
    
    
    
    
    