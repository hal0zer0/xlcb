# -*- coding: utf-8 -*-
from xl.nls import gettext as _
#from xl import settings as xlsettings
from xl import event
import gtk
import os
import datetime
import xlcbpub
import xlcbconfig
#import xlcbgui


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Base plugin stuff
def enable(exaile):
  """ Called by Exaile on program start """
  if (exaile.loading):
    event.add_callback(_enable, 'exaile_loaded')
  else:
    _enable(None, exaile, None)
 
def disable(exaile):
  """ Called by Exaile when plugin disabled """
  print('XLCB Disabled')
 
def _enable(eventname, exaile, nothing):
  """ Called by Exaile when plugin enabled """ 
  print('XLCB Loaded')
  plugin = xlcb(exaile)
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Create menu item, attach launch to xlcbpub
class xlcb:
  def __init__(self, exaile):
    # Make basic onformation available to plugin
    self.pluginName = "XLCB"
    self.exaile = exaile
    # Add XLCB item to Tools menu
    self.MENU_ITEM = gtk.MenuItem(_('XLCB'))
    self.MENU_ITEM.connect('activate', self.menu_cb, exaile)
    exaile.gui.builder.get_object('tools_menu').append(self.MENU_ITEM)
    self.MENU_ITEM.show()
    
    
  def menu_cb(self, unused, exaile):
    publisher = xlcbpub.XLCBPublisher(exaile)
    publisher.show_gui()
    
  





    
    
    