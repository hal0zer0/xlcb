# -*- coding: utf-8 -*-
import transcoder

class XLCBPublisher:
  def __init__(self, playlist, settings):
    self.playlist = playlist
    self.settings = settings
    self.encode()
  
  def encode(self):
    #Settings for the whole transcoding
    tc = transcoder.Transcoder()


    
    for track in self.playlist:
    
      #settings that change per-file
      source = track["location"]
      dest = self.set_filename(track)
      
      
      #source="/media/AA0C-FA89/Music/Tumbler.mp3"
      #dest="/home/josh/trans-test/tumbler.ogg"
      tc = transcoder.Transcoder()
      tc.set_format(self.settings["outputFormat"]) # was "Ogg Vorbis"
      #tc.set_quality(224)
      
      tc.set_input(source)
      tc.set_output(dest)
      print " ".join(["Starting conversion of", source, "to", dest])
      tc.start_transcode(self.settings)
      
  
  def set_filename(self, track):
    #TODO:  Parse the track properly based on options
    path = self.settings["outputDir"]
    name = "_".join([track["artist"], track["title"], ".ogg"]).replace(" ","_")
    return "/".join([path, name])