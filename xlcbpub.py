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
    if self.settings["outputFormat"] == "Ogg Vorbis":
      self.ext = ".ogg"
    elif self.settings["outputFormat"] == "FLAC":
      self.ext = ".flac"
    elif self.settings["outputFormat"] == "copy":
      pass
    
    for track in self.playlist:
      source = track["location"]
      dest = self.set_filename(track)
      tc = transcoder.Transcoder(self.logbox_cb, self.FORMATS)
      tc.set_input(source)
      tc.set_output(dest)
      tc.start_transcode(self.settings)
      
  
  def set_filename(self, track):
    #TODO:  Parse the track properly based on options
    path = self.settings["outputDir"]
    name = "_".join([track["artist"], track["title"]]).replace(" ","_") + self.ext
    return "/".join([path, name])
    
