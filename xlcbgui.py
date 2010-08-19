# -*- coding: utf-8 -*-
import pygtk
import gtk
import gtk.glade
import os
import xlcbconfig

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
    
    self.config = xlcbconfig.config
    
    
  
  def _add_manual_combos(self):
    # It is hell trying to work with Glade's combo boxes
    # so I just added GTK ones manually.  Sue me.  
    self.convertBox = gtk.combo_box_new_text()
    self.processingTable.attach(self.convertBox, 5,9,1,2)
    self.convertBox.connect("changed", self.cBox_cb)
    self.qualityBox = gtk.combo_box_new_text()
    #self.qualityBox.connect("changed", self.qbox_cb)
    self.processingTable.attach(self.qualityBox, 5,9,2,3)
    #self.processingTable.show_all()
    

    #try:
      #self.processingTable.remove(self.qualityBox)
    #except:
      #pass
  
  def _goButton_cb(self):
    pass
  
  
  def update_qbox(self, qualityList):
    pass
  
  
  def show(self, unneeded, exaile):
    self.window.show_all()
    gtk.main()
    
      #def populate(self):
    ##Set UI elements to match settings pulled from Exaile
    #settingsDict = self.get_settings_from_exaile()
    
    #self.builder.get_object("albumNameEntry").set_text(settingsDict["albumName"])
    #self.builder.get_object("albumInFileNameCheckbox").set_active(settingsDict["albumInFileName"])
    #self.builder.get_object("authorNameEntry").set_text(settingsDict["authorName"])
    #self.builder.get_object("outputDirEntry").set_text(settingsDict["outputDir"])
    
    
    #self.update_qbox(settingsDict["outputFormat"])
    ##self.qualityBox.
    
  #Callbacks------------------------------------------------------------------
  def cBox_cb(self, box):
    format = box.get_active_text()
    print "ConvertBox CB called, format = %s" % format
    self.update_qbox(format)