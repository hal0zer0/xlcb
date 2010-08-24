# -*- coding: utf-8 -*-
from xl.nls import gettext as _
from xl import settings as xlsettings
import os

def get_settings_from_exaile():
  pluginSettings = {}
  for settingName in defaultSettings:
    # ie plugin/XLCB/albumName
    optionPath = "/".join(("plugin", pluginName, settingName))
    # Use Exaile's settings if there, defaults if not
    pluginSettings[settingName] = xlsettings.get_option(optionPath, defaultSettings[settingName])
  return pluginSettings
  
  
def save_settings_to_exaile(gui, cbox, qbox): 
  #"gui" is the builder object from glade
  #cbox and qbox are the two GTK combo boxes I had to add manually
  #because working with the Glade combo boxes is insanity
  toSave = [["albumName", gui.get_object("albumNameEntry").get_text()],
	    ["albumInFileName",  gui.get_object("albumInFileNameCheckbox").get_active()],
	    ["authorName", gui.get_object("authorNameEntry").get_text()],
	    ["outputDir", gui.get_object("outputDirEntry").get_text()],
	    ["outputFormat", cbox.get_active_text()],
	    ["quality", qbox.get_active_text()]]
	    
  for setting in toSave:
    #0 is setting name, 1 is the data to be saved
    print "saving setting %s" % setting[0] , setting[1]
    optionPath = "/".join(("plugin", pluginName, setting[0]))
    xlsettings.set_option(optionPath, setting[1])
    
    
#--------------------------------------------------------------------------    
pluginName = "XLCB"
defaultSettings = {"albumName":        "XLCB Comp",
                   "albumInFileName":  False,
                   "authorName":       "Unknown",
                   "outputDir":        os.path.expanduser('~'),
                   "smartNaming":      True,
                   "outputFormat":     "FLAC",
                   "quality":          None} 

#config = get_settings_from_exaile()