# -*- coding: utf-8 -*-
import transcoder
import xlcbformats
import datetime
import time
import threading

class Publisher:
  def __init__(self, config, exaile, pbar_cb):
    self.config = config
    self.exaile = exaile
    self.FORMATS = xlcbformats.get_formats()
    self.threadCount = 0
    self.finishedCount = 0
    self.pbar_cb = pbar_cb

  def begin(self):
    self.playlist = self.get_playlist()
    self.encode()
    
  def get_filename(self, track, config):
    #TODO:  Parse the track properly based on options
    nameList = []
    path = config["outputDir"]
    ext = self.FORMATS[config["outputFormat"]]["extension"]
    artist = track["artist"].replace(" ","_")
    title = track["title"].replace(" ","_")
    delim = "-"
    nameList.append(artist)
    if config["albumInFileName"]:
      nameList.append(config["albumName"].replace(" ","_"))
    nameList.append(title)
    name = delim.join(nameList) + ".%s" % ext
    print "/".join([path, name])
    return "/".join([path, name])
    

  def encode(self):
    self.total = len(self.playlist)
    tc = transcoder.Transcoder(self.FORMATS)
    for track in self.playlist:
      
      source = track["location"]
      dest = self.get_filename(track, self.config)
      tc = transcoder.Transcoder(self.FORMATS)
      tc.set_input(source)
      tc.set_output(dest)
      tc.set_format(self.config["outputFormat"])
      #Some formats use integer quality settings, others use floats.  
      #The integers have to be passed as integers, the floats as floats.  
      #I now must read the setting and determine what it is in order
      #to cast it properly.  I haven't found a better way.  
      if "." in self.config["quality"]:
	tc.set_quality(float(self.config["quality"]))
      else:
	tc.set_quality(int(self.config["quality"]))
      
      self.threadCount += 1
      print "Starting encode, threadcount", self.threadCount
      tc.start_transcode(self.config["outputDir"], self.decrement)
      time.sleep(1)

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
      print xlcbTrack["title"]
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
    
  def decrement(self):
    print "finished, reducing thread count from", self.threadCount
    self.threadCount -= 1
    self.finishedCount += 1
    self.pbar_cb(self.finishedCount, self.total)


