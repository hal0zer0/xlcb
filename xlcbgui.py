# -*- coding: utf-8 -*-
from xl.nls import gettext as _
import pygtk
import gtk
import gtk.glade
import os
import xlcbconfig
import xlcbformats
import finalize

class XLCBGUI:
  def __init__(self):
    # Load prebuilt Glade GUI and create shared object properties
    gladefile = os.path.dirname(__file__) + "/xlcbgui.glade"
    self.builder = gtk.Builder()
    self.builder.add_from_file(gladefile)
    self.window = self.builder.get_object("window1")
    # Button connections for GUI
    buttonActions = { "on_beginButton_clicked" : self._goButton_cb,
            "on_MainWindow_destroy" : gtk.main_quit }
    self.builder.connect_signals(buttonActions)
    # For the two special combo boxes...
    self.processingTable = self.builder.get_object("processingTable")
    self._add_manual_combos()
    self.formats = xlcbformats.get_formats()
    self.config = xlcbconfig.config
    self._set_gui_from_config()
    
  
  def _add_manual_combos(self):
    # It is hell trying to work with Glade's combo boxes
    # so I just added GTK ones manually.  Sue me.  
    self.convertBox = gtk.combo_box_new_text()
    self.processingTable.attach(self.convertBox, 5,9,1,2)
    self.convertBox.connect("changed", self.cBox_cb)
    self.qualityBox = gtk.combo_box_new_text()
    self.processingTable.attach(self.qualityBox, 5,9,2,3)

    
  def show(self):
    self.window.show_all()
    gtk.main()
    #return self.config
    
  
  def _set_gui_from_config(self):
    ##Set UI elements to match settings pulled from Exaile
    #settingsDict = self.get_settings_from_exaile()
    widget = self.builder.get_object
    
    widget("albumNameEntry").set_text(self.config["albumName"])
    widget("albumInFileNameCheckbox").set_active(self.config["albumInFileName"])
    widget("authorNameEntry").set_text(self.config["authorName"])
    widget("outputDirEntry").set_text(self.config["outputDir"])
    #And the two special combo boxes
    self._populate_cBox()
    self._populate_qBox()
    #Setting active selection to last saved.
    self.convertBox.set_active(self._find_index_of("format", self.config["outputFormat"]))
    self.qualityBox.set_active(self._find_index_of("quality", self.config["quality"]))
    
    
  def _find_index_of(self, whichbox, tofind):
    #TODO: come up with a more efficient way of finding the index # of this entry
    if whichbox == "format":
      i = 0
      for format in self.formats:
        if format == tofind:
	  return i
        else:
	  i += 1
    elif whichbox == "quality":
      i = 0
      format = self.convertBox.get_active_text()
      for quality in self.formats[format]["raw_steps"]:
	print str(quality), tofind
	if str(quality) == tofind:
	  return i
	else:
	  i += 1
    print "No Match!  Faking it!"
    return 0
    #if whichbox = "quality"
      
  
  def _populate_cBox(self):
    #Clear out existing items from quality box
    for i in range(len(self.convertBox.get_model())):
      self.convertBox.remove_text(0)
    for format in self.formats:
      self.convertBox.append_text(format)    

  
  def _populate_qBox(self):
    audioformat = self.config["outputFormat"]
    data = self.formats[audioformat]["raw_steps"]
    #Add items to quality box
    for qvalue in data:
      self.qualityBox.append_text(str(qvalue))
      

  def _refresh_qBox(self):
    #Clear out existing items from quality box
    print "refreshing qualities"
    for i in range(len(list(self.qualityBox.get_model()))):
      self.qualityBox.remove_text(0)
    #self._populate_qBox()
    audioformat = self.convertBox.get_active_text()
    data = self.formats[audioformat]["raw_steps"]
    #Add items to quality box
    for qvalue in data:
      self.qualityBox.append_text(str(qvalue))
    
    
  #Callbacks------------------------------------------------------------------
  def cBox_cb(self, box):
    format = box.get_active_text()
    print "ConvertBox CB called, format = %s" % format
    self._refresh_qBox()
    
  def _goButton_cb(self, buttonProbably):
    xlcbconfig.save_settings_to_exaile(self.builder, self.convertBox, self.qualityBox)
    self.config = xlcbconfig.get_settings_from_exaile()
    finalizer = finalize.Finalizer(self.config)
    