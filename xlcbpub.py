# -*- coding: utf-8 -*-
import transcoder
import xlcbformats
import datetime

FORMATS = xlcbformats.get_formats()
def begin(config, exaile, pbar_cb):
  playlist = get_playlist(exaile)
  encode(playlist, config)
  
def get_filename(track, config):
  #TODO:  Parse the track properly based on options
  nameList = []
  path = config["outputDir"]
  ext = FORMATS[config["outputFormat"]]["extension"]
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
  

def encode(playlist, config):
  for track in playlist:
    source = track["location"]
    dest = get_filename(track, config)
    tc = transcoder.Transcoder(FORMATS)
    tc.set_input(source)
    tc.set_output(dest)
    tc.set_format(config["outputFormat"])
    #Some formats use integer quality settings, others use floats.  
    #The integers have to be passed as integers, the floats as floats.  
    #I now must read the setting and determine what it is in order
    #to cast it properly.  I haven't found a better way.  
    if "." in config["quality"]:
      print "seems float:", config["quality"]
      tc.set_quality(float(config["quality"]))
    else:
      print "seems int:", config["quality"]
      tc.set_quality(int(config["quality"]))
    tc.start_transcode(config["outputDir"])

def get_playlist(exaile):
  # Reads the active playlist and converts to more easily parsed formatted
  # for the publisher
  xlcbPlaylist = []
  raw_pl = exaile.gui.main.get_selected_playlist().playlist    
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
  


