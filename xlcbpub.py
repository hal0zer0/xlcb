# -*- coding: utf-8 -*-
import transcoder
import xlcbformats
import datetime
import time
import threading

class Publisher:
  def __init__(self, config, exaile):
    self.config = config
    self.exaile = exaile
    self.FORMATS = xlcbformats.get_formats()
    self.threadCount = 0
    self.finishedCount = 0
    #self.pbar_cb = pbar_cb
    self.transcoder = transcoder.Transcoder()
    self.running = False
    self.cont = None
    self.playlist = self.get_playlist()
    

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
    self.running = True
    
    self.cont = threading.Event()
    
    self.total = self.threadCount
    

    
    for track in self.playlist:
      self.cont.clear()
      source = track["location"]
      dest = self.get_filename(track, self.config)
      
      self.transcoder = transcoder.Transcoder()
      self.transcoder.set_format(self.config["outputFormat"])
      if "." in self.config["quality"]:
        self.transcoder.set_quality(float(self.config["quality"]))
      else:
        self.transcoder.set_quality(int(self.config["quality"]))
      self.transcoder.end_cb = self._end_cb
      
      self.transcoder.set_input(source)
      self.transcoder.set_output(dest)
      
      #Some formats use integer quality settings, others use floats.  
      #The integers have to be passed as integers, the floats as floats.  
      #I now must read the setting and determine what it is in order
      #to cast it properly.  I haven't found a better way.  
      if "." in self.config["quality"]:
	self.transcoder.set_quality(float(self.config["quality"]))
      else:
	self.transcoder.set_quality(int(self.config["quality"]))
      
      self.threadCount += 1
      print "Starting encode, threadcount", self.threadCount
      self.transcoder.start_transcode()
      print "transcode started, hitting cont.wait"
      self.cont.wait(1)
      print "wait over"
      if not self.running:
	break
	
      # The FOR loop needs to update the GUI between tracks
      
      
  def _end_cb(self):
    print "apparently con.wait() worked because I'm in _end_cb"
    self.cont.set()
    self.running = False

  def stop(self):
    self.running = False
    self.transcoder.stop()

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


    def get_progress(self):
        if not self.current or not self.current_len:
            return self.progress
        incr = self.current_len / self.duration
        pos = self.transcoder.get_time()/float(self.current_len)
        return 69
        #return self.progress + pos*incr
