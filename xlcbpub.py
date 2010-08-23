# -*- coding: utf-8 -*-
import transcoder
import xlcbformats
import xlcbgui

class XLCBPublisher:
  def __init__(self, exaile):
    self.playlist = self.get_playlist 
    self.formats = xlcbformats.get_formats()
    self.exaile = exaile


  def show_gui(self):
    gui = xlcbgui.XLCBGUI()
    config = gui.show()
    

  def encode(self):
    for track in self.playlist:
      source = track["location"]
      dest = self.set_filename(track)
      tc = transcoder.Transcoder(self.logbox_cb, self.FORMATS)
      tc.set_input(source)
      tc.set_output(dest)
      tc.set_format(self.settings["outputFormat"])
      #Some formats use integer quality settings, others use floats.  
      #The integers have to be passed as integers, the floats as floats.  
      #I now must read the setting and determine what it is in order
      #to cast it properly.  I haven't found a better way.  
      if "." in self.settings["quality"]:
	print "seems float:", self.settings["quality"]
      else:
	print "seems int:", self.settings["quality"]
      tc.start_transcode(self.settings)
      
  
  def set_filename(self, track):
    #TODO:  Parse the track properly based on options
    nameList = []
    path = self.settings["outputDir"]
    ext = self.FORMATS[self.settings["outputFormat"]]["extension"]
    artist = track["artist"].replace(" ","_")
    title = track["title"].replace(" ","_")
    delim = "-"
    nameList.append(artist)
    if self.settings["albumInFileName"]:
      nameList.append(self.settings["albumName"]).replace(" ","_")
    nameList.append(title)
    name = delim.join(nameList) + ".%s" % ext
    print "/".join([path, name])
    return "/".join([path, name])
    
  #def startBuilding(self, arg):
    # Called when Begin button clicked.  
    #self.save_settings_to_exaile()
    #self.logbox_cb(_("XLCB encodes using multiple threads.  \
                      #Files may finish encoding in an order \
                      #different than they started.\n\n"))
    
    #pub = xlcbpub.XLCBPublisher(self.playlist, 
                                #self.get_settings_from_exaile(), 
                                #self.logbox_cb)
                                

    
  #def logbox_cb(self, text):
    #logbox = self.builder.get_object("logBox")
    ## This is an ugly hack for counting the completed items
    #if "FINISHED: " in text:
      #self.finished += 1
      #logbox.get_buffer().insert_at_cursor("%i complete\n" % self.finished )
    #logbox.get_buffer().insert_at_cursor(text + "\n")
    
  
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
      xlcbTrack["lengthSeconds"] = int(
                                   round(
                                   float(
                                   raw_track.get_tag_display("__length")), 0))
      #I'd love to know a better way to chop hours off.  
      xlcbTrack["lengthMinutes"] = str(datetime.timedelta(
                                       seconds=xlcbTrack["lengthSeconds"]))[2:]
      xlcbTrack["location"] = raw_track.get_tag_display("__loc")
      xlcbPlaylist.append(xlcbTrack)
    return xlcbPlaylist
    


