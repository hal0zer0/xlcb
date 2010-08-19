# -*- coding: utf-8 -*-
from xl.nls import gettext as _
#from xl import settings as xlsettings
from xl import event
import gtk
import os
import datetime
import xlcbpub
import xlcbconfig
import xlcbgui

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
    self.gui = xlcbgui.XLCBGUI()
    # Add XLCB item to Tools menu
    self.MENU_ITEM = gtk.MenuItem(_('XLCB'))
    self.MENU_ITEM.connect('activate', self.gui.show, exaile)
    exaile.gui.builder.get_object('tools_menu').append(self.MENU_ITEM)
    self.MENU_ITEM.show()
    
    
    self.finished = 0
    self.playlist = self.get_playlist()
    self.formats = self.get_formats()
    configObject = xlcbconfig.Config()
    self.settings = configObject.settings
        
  
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


    
  def convertBox_cb(self, box):
    format = box.get_active_text()
    print "ConvertBox CB called, format = %s" % format
    self.update_qbox(format)
    
    

    
    
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



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# 


    
    
    
    
    
    
    