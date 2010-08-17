# -*- coding: utf-8 -*-
from xl.nls import gettext as _
from xl import settings as xlsettings
from xl import event

import pygtk
import gtk
import gtk.glade
import os
import datetime
import xlcbpub

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Base functions for pluginability
def enable(exaile):
    if (exaile.loading):
        event.add_callback(_enable, 'exaile_loaded')
    else:
        _enable(None, exaile, None)
 
def disable(exaile):
    print('XLCB Disabled')
 
def _enable(eventname, exaile, nothing):
    print('XLCB Loaded')
    plugin = xlcb(exaile)
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Actual plugin code
class xlcb:
  
  def __init__(self, exaile):
    # Make basic onformation available to plugin
    self.pluginName = "XLCB"
    self.exaile = exaile
    
    # Add XLCB item to Tools menu
    self.MENU_ITEM = gtk.MenuItem(_('XLCB'))
    self.MENU_ITEM.connect('activate', self.show_gui, exaile)
    exaile.gui.builder.get_object('tools_menu').append(self.MENU_ITEM)
    self.MENU_ITEM.show()


  def show_gui(self, something, exaile):
    #Load up Glade GUI file
    self.gladefile = os.path.dirname(__file__) + "/xlcbgui.glade"
    self.builder = gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    
    # Button connections for GUI
    buttonActions = { "on_beginButton_clicked" : self.startBuilding,
            "on_MainWindow_destroy" : gtk.main_quit }
    self.builder.connect_signals(buttonActions)
    
    self.window = self.builder.get_object("window1")
    self.populate()
    self.window.show_all()
    gtk.main()
    
    
  def get_playlist(self):
    # Reads the active playlist and converts to more easily parsed formatted
    # for the publisher
    xlcbPlaylist = []
    raw_pl = self.exaile.gui.main.get_selected_playlist().playlist
    
    #Read each track, form list of dictionaries for publisher
    for raw_track in raw_pl:
      xlcbTrack = {}
      xlcbTrack["artist"] = raw_track.get_tag_display("artist")
      xlcbTrack["title"] = raw_track.get_tag_display("title")
      xlcbTrack["lengthSeconds"] = int(round(float(raw_track.get_tag_display("__length")), 0))
      #xlcbTrack["location"]
      #Using string slicing as an ugly hack to remove hours from formatted time
      xlcbTrack["lengthMinutes"] = str(datetime.timedelta(seconds=xlcbTrack["lengthSeconds"]))[2:]
      xlcbTrack["location"] = raw_track.get_tag_display("__loc")
      #print xlcbTrack
      xlcbPlaylist.append(xlcbTrack)
    #print raw_track.list_tags()
    return xlcbPlaylist

  def startBuilding(self, arg):
    # Called when Begin button clicked.  
    self.save_settings()
    #playlist = self.get_playlist()
    print "XLCB Build started"
    print type(arg)
    pub = xlcbpub.XLCBPublisher(self.get_playlist(), self.get_settings())
    #pub.encode()
    
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Loading and saving user settings
  def populate(self):
    settingsDict = self.get_settings()
    self.builder.get_object("albumNameEntry").set_text(settingsDict["albumName"])
    self.builder.get_object("albumInFileNameCheckbox").set_active(settingsDict["albumInFileName"])
    self.builder.get_object("authorNameEntry").set_text(settingsDict["authorName"])
    self.builder.get_object("outputDirEntry").set_text(settingsDict["outputDir"])
    
    
  def get_settings(self):
    #                        Name of setting:   default value
    self.defaultSettings = {"albumName":        "XLCB Comp",
                            "albumInFileName":  False,
                            "authorName":       "Unknown",
                            "outputDir":        os.path.expanduser('~'),
                            "smartNaming":      True,
                            "outputFormat":     "FLAC"}
    
    pluginSettings = {}
    for settingName in self.defaultSettings:
      optionPath = "/".join(("plugin", self.pluginName, settingName))
      # Use Exaile's settings if there, defaults if not
      pluginSettings[settingName] = xlsettings.get_option(optionPath, self.defaultSettings[settingName])

    return pluginSettings
    
    
  def save_settings(self):
    if self.builder.get_object("copyOnlyButton").get_active():
      outputFormat = "copy"
    elif self.builder.get_object("convertOggButton").get_active():
      outputFormat = "Ogg Vorbis"
    elif self.builder.get_object("convertFlacButton").get_active():
      outputFormat = "FLAC"
    else:
      print "Invalid format: no button shows as active"
      
    #List of setting names and data to save
    toSave = [["albumName", self.builder.get_object("albumNameEntry").get_text()],
              ["albumInFileName",  self.builder.get_object("albumInFileNameCheckbox").get_active()],
              ["authorName", self.builder.get_object("authorNameEntry").get_text()],
              ["outputDir", self.builder.get_object("outputDirEntry").get_text()],
              ["outputFormat", outputFormat]]
              
    for setting in toSave:
      #0 is setting name, 1 is the data to be saved
      optionPath = "/".join(("plugin", self.pluginName, setting[0]))
      xlsettings.set_option(optionPath, setting[1])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 


    
    
    
    
    
    
    