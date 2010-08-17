# -*- coding: utf-8 -*-
import transcoder

class XLCBPublisher:
  def __init__(self, playlist, settings, logbox_cb, formats):
    self.playlist = playlist
    self.settings = settings
    self.logbox_cb = logbox_cb
    self.FORMATS = formats
    
    self.encode()


  def encode(self):
    for track in self.playlist:
      source = track["location"]
      dest = self.set_filename(track)
      tc = transcoder.Transcoder(self.logbox_cb, self.FORMATS)
      tc.set_input(source)
      tc.set_output(dest)
      tc.set_format(self.settings["outputFormat"])
      try:
	tc.set_quality(int(self.settings["quality"]))
      except:
	tc.set_quality(float(self.settings["quality"]))
      tc.start_transcode(self.settings)
      
  
  def set_filename(self, track):
    #TODO:  Parse the track properly based on options
    path = self.settings["outputDir"]
    ext = ".%s" % self.settings["outputFormat"]
    print ext
    name = "_".join([track["artist"], track["title"]]).replace(" ","_") + "." + self.FORMATS[self.settings["outputFormat"]]["extension"]
    return "/".join([path, name])
    
