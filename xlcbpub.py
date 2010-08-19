# -*- coding: utf-8 -*-
import transcoder
import xlcbformats

class XLCBPublisher:
  def __init__(self, playlist, settings, logbox_cb):
    self.playlist = playlist
    self.settings = settings
    self.logbox_cb = logbox_cb
    self.formats = xlcbformats.get_formats()
    
    self.encode()


  def encode(self):
    for track in self.playlist:
      source = track["location"]
      dest = self.set_filename(track)
      tc = transcoder.Transcoder(self.logbox_cb, self.FORMATS)
      tc.set_input(source)
      tc.set_output(dest)
      tc.set_format(self.settings["outputFormat"])
      #Some formats use integer quality settings, others use floats.  
      #Since the quality setting has to be converted to strings for
      #the comboboxes, I need this try/except to convert back to 
      #proper numerical format.  It's pretty ugly.  Improve it =)
      try:
	tc.set_quality(int(self.settings["quality"]))
      except:
	tc.set_quality(float(self.settings["quality"]))
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
    
