# -*- coding: utf-8 -*-
from xl.nls import gettext as _
import gtk, gtk.glade
import xlcbconfig, xlcbformats
import threading, gobject
import imp, os
publisher = imp.load_source("publisher",
        os.path.join(os.path.dirname(__file__), "xlcbpub.py"))

class XLCBGUI:
  def __init__(self, exaile):
    self.exaile = exaile
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
    #Working with items in Glade's combo boxes is awful, so I 
    #added two of them manually with GTK
    self._add_manual_combos()
    self.formats = xlcbformats.get_formats()
    self.config = xlcbconfig.get_settings_from_exaile()
    self._set_gui_from_config()
    self.status = self.builder.get_object("statusLabel")
    self.show()
    
    
  
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
    
  
  def _set_gui_from_config(self):
    ##Set UI elements to match settings pulled from Exaile
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
      for i, format in enumerate(self.formats):
        if format == tofind:
	  return i
    elif whichbox == "quality":
      format = self.convertBox.get_active_text()
      for i, quality in enumerate(self.formats[format]["raw_steps"]):
	print str(quality), tofind
	if str(quality) == tofind:
	  return i
    raise KeyError, "Invalid quality setting"
      
  
  def _populate_cBox(self):
    #Clear out existing items from quality box
    for i in range(len(self.convertBox.get_model())):
      self.convertBox.remove_text(0)
    #Add new items
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
      
  
  def _update_pbar(self, complete, total):
    fraction = float(complete)/float(total)
    print "fraction  =", fraction
    self.pbar.set_fraction(fraction)
    text = "Building playlist, %i complete" % complete
    self.status.set_text(text)

    
  
  
  #Running the build---------------------------------------------------------
  def _gogogo(self):
    self.pbar = self.builder.get_object("progressBar")
    self.pub = publisher.Publisher(self.config, self.exaile)
    encoder = EncodeThread(self.pub, self.pbar)
    encoder.run()
    #pub.encode()
    
  
    
  #Callbacks------------------------------------------------------------------
  def cBox_cb(self, box):
    format = box.get_active_text()
    print "ConvertBox CB called, format = %s" % format
    self._refresh_qBox()
    
  def _goButton_cb(self, buttonProbably):
    self.status.set_text("Building playlist...")
    xlcbconfig.save_settings_to_exaile(self.builder, self.convertBox, self.qualityBox)
    self.config = xlcbconfig.get_settings_from_exaile()
    self._gogogo()
    
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # #    
class EncodeThread(threading.Thread):
  def __init__(self, pub, pbar):
    threading.Thread.__init__(self)
    self.setDaemon(True)
    self.pub = pub
    self.pbar = pbar

  def stop_thread(self):
    self.pub.stop()

  def _update_pbar(self, complete=0, total=0):
    fraction = float(complete)/float(total)
    print "fraction  =", fraction
    self.pbar.set_fraction(fraction)
    text = "Building playlist, %i complete" % complete
    self.status.set_text(text)
    
    
  def progress_update(self, progress=None):
    if progress is None:
      progress = .69
      progress = self.imp.get_progress()*100
      event.log_event("progress_update", self, progress)
      return True

  def run(self):
    id = gobject.timeout_add_seconds(1, self.progress_update)
    #self.imp.do_import()
    self.pub.encode()
    gobject.source_remove(id)
    self.progress_update(100)