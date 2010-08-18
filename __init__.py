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
    self.finished = 0
    self.playlist = self.get_playlist()
    self.formats = self.get_formats()
        


  def show_gui(self, unneeded, exaile):
    #Load up Glade GUI file
    self.gladefile = os.path.dirname(__file__) + "/xlcbgui.glade"
    self.builder = gtk.Builder()
    self.builder.add_from_file(self.gladefile)
    
    # Button connections for GUI
    buttonActions = { "on_beginButton_clicked" : self.startBuilding,
            "on_MainWindow_destroy" : gtk.main_quit }
    self.builder.connect_signals(buttonActions)
    
    self.window = self.builder.get_object("window1")
    self.processingTable = self.builder.get_object("processingTable")
    
    
    #Had to add two ComboBoxes manually, could not get Glade's working
    self.make_convertBox()
    self.make_qbox()
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
    self.save_settings_to_exaile()
    #playlist = self.get_playlist()
    self.logbox_cb(_("XLCB encodes using multiple threads.  Files may finish encoding in an order different than they started.\n\n"))
    
    pub = xlcbpub.XLCBPublisher(self.playlist, self.get_settings_from_exaile(), self.logbox_cb, self.get_formats())
    #pub.encode()
    
  def logbox_cb(self, text):
    logbox = self.builder.get_object("logBox")
    # This is an ugly hack for counting the completed items
    if "FINISHED: " in text:
      self.finished += 1
      logbox.get_buffer().insert_at_cursor("%i complete\n" % self.finished )
    logbox.get_buffer().insert_at_cursor(text + "\n")

    
  def get_formats(self):
    FORMATS = {
        "Ogg Vorbis" : {
            "default"   : 0.5,
            "raw_steps" : [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "kbs_steps" : [64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
            "command"   : "vorbisenc quality=%s ! oggmux",
            "extension" : "ogg",
            "plugins"   : ["vorbisenc", "oggmux"],
            "desc"      : _("Vorbis is an open source, lossy audio codec with "
                    "high quality output at a lower file size than MP3.")
            },
        "FLAC" : {
            "default"   : 5,
            "raw_steps" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "kbs_steps" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "command"   : "flacenc quality=%s",
            "extension" : "flac",
            "plugins"   : ["flacenc"],
            "desc"      : _("Free Lossless Audio Codec (FLAC) is an open "
                    "source codec that compresses but does not degrade audio "
                    "quality.")
            },
        "AAC"       : {
            "default"   : 160000,
            "raw_steps" : [32000, 48000, 64000, 96000, 128000, 160000,
                    192000, 224000, 256000, 320000],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "faac bitrate=%s ! ffmux_mp4",
            "extension" : "m4a",
            "plugins"   : ["faac", "ffmux_mp4"],
            "desc"      : _("Apple's proprietary lossy audio format that "
                    "achieves better sound quality than MP3 at "
                    "lower bitrates.")
            },
        "MP3 (VBR)" : {
            "default"   : 160,
            "raw_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "lame vbr=4 vbr-mean-bitrate=%s",
            "extension" : "mp3",
            "plugins"   : ["lame"],
            "desc"      : _("A proprietary and older, but also popular, lossy "
                    "audio format. VBR gives higher quality than CBR, but may "
                    "be incompatible with some players.")
            },
        "MP3 (CBR)" : {
            "default"   : 160,
            "raw_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "lame bitrate=%s",
            "extension" : "mp3",
            "plugins"   : ["lame"],
            "desc"      : _("A proprietary and older, but also popular, "
                    "lossy audio format. CBR gives less quality than VBR, "
                    "but is compatible with any player.")
            },
        "WavPack" : {
            "default"   : 2,
            "raw_steps" : [1,2,3,4],
            "kbs_steps" : [1,2,3,4],
            "command"   : "wavpackenc mode=%s",
            "extension" : "wv",
            "plugins"   : ["wavpackenc"],
            "desc"      : _("A very fast Free lossless audio format with "
                    "good compression."),
            },
        }
    return FORMATS


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Dealing with the non-Glade ComboBoxes I had to add

  def make_convertBox(self):
    self.convertBox = gtk.combo_box_new_text()
    self.convertBox.connect("changed", self.convertBox_cb)
    self.processingTable.attach(self.convertBox, 5,9,1,2)
    for name in self.formats:
      self.convertBox.append_text(name)
    
  def convertBox_cb(self, box):
    format = box.get_active_text()
    print "ConvertBox CB called, format = %s" % format
    self.update_qbox(format)
    
    
  def make_qbox(self):
    try:
      self.processingTable.remove(self.qualityBox)
    except:
      pass
    self.qualityBox = gtk.combo_box_new_text()
    self.qualityBox.connect("changed", self.qbox_cb)
    self.processingTable.attach(self.qualityBox, 5,9,2,3)
    self.processingTable.show_all()
    
    
  def update_qbox(self, format):
    self.make_qbox()
    if format in self.formats:
      data = self.formats[format]["raw_steps"]
    else: 
      data = []
    for qvalue in data:
      self.qualityBox.append_text(str(qvalue))
    
    
  def qbox_cb(self, format):
    pass

  











# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Loading and saving user settings
  def populate(self):
    #Set UI elements to match settings pulled from Exaile
    settingsDict = self.get_settings_from_exaile()
    
    self.builder.get_object("albumNameEntry").set_text(settingsDict["albumName"])
    self.builder.get_object("albumInFileNameCheckbox").set_active(settingsDict["albumInFileName"])
    self.builder.get_object("authorNameEntry").set_text(settingsDict["authorName"])
    self.builder.get_object("outputDirEntry").set_text(settingsDict["outputDir"])
    
    
    self.update_qbox(settingsDict["outputFormat"])
    #self.qualityBox.
  
  def get_settings_from_exaile(self):
    #Gets last saved settings from Exaile
    #                        Name of setting:   default value
    self.defaultSettings = {"albumName":        "XLCB Comp",
                            "albumInFileName":  False,
                            "authorName":       "Unknown",
                            "outputDir":        os.path.expanduser('~'),
                            "smartNaming":      True,
                            "outputFormat":     "FLAC",
                            "quality":          None} 
    pluginSettings = {}
    for settingName in self.defaultSettings:
      optionPath = "/".join(("plugin", self.pluginName, settingName))
      # Use Exaile's settings if there, defaults if not
      pluginSettings[settingName] = xlsettings.get_option(optionPath, self.defaultSettings[settingName])

    return pluginSettings
    
    
  def save_settings_to_exaile(self): 
    #List of setting names and data to save
    toSave = [["albumName", self.builder.get_object("albumNameEntry").get_text()],
              ["albumInFileName",  self.builder.get_object("albumInFileNameCheckbox").get_active()],
              ["authorName", self.builder.get_object("authorNameEntry").get_text()],
              ["outputDir", self.builder.get_object("outputDirEntry").get_text()],
              ["outputFormat", self.convertBox.get_active_text()],
              ["quality", str(self.qualityBox.get_active_text())]]
              
    for setting in toSave:
      #0 is setting name, 1 is the data to be saved
      print "saving setting %s" % setting[0]
      optionPath = "/".join(("plugin", self.pluginName, setting[0]))
      xlsettings.set_option(optionPath, setting[1])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 


    
    
    
    
    
    
    