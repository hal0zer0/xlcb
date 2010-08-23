# -*- coding: utf-8 -*-
import gtk
import pygtk

class Finalizer():
  def __init__(self, config):
    window = gtk.Window()
    #window.set_size_request(400,300)
    sw = gtk.ScrolledWindow()
    window.add(sw)
    self.vbox = gtk.VBox(homogeneous=True)
    sw.add_with_viewport(self.vbox)
    
    progbar1 = gtk.ProgressBar()
    progbar2 = gtk.ProgressBar()
    progbar3 = gtk.ProgressBar()
    progbar4 = gtk.ProgressBar()
    progbar5 = gtk.ProgressBar()
    progbar6 = gtk.ProgressBar()
      
    self.vbox.pack_start(progbar1)
    self.vbox.pack_start(progbar2)
    self.vbox.pack_start(progbar3)
    self.vbox.pack_start(progbar4)
    self.vbox.pack_start(progbar5)
    self.vbox.pack_start(progbar6)
    
    window.show_all()
    gtk.main()
  