# -*- coding: utf-8 -*-
# Copyright (C) 2008-2009 Adam Olsen
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
#
# The developers of the Exaile media player hereby grant permission
# for non-GPL compatible GStreamer and Exaile plugins to be used and
# distributed together with GStreamer and Exaile. This permission is
# above and beyond the permissions granted by the GPL license by which
# Exaile is covered. If you modify this code, you may extend this
# exception to your version of the code, but you are not obligated to
# do so. If you do not wish to do so, delete this exception statement
# from your version.


import pygst
pygst.require("0.10")
import gst
import os

from xl.nls import gettext as _

"""
    explanation of format dicts:
    default:    the default quality to use, must be a member of raw_steps.
    raw_steps:  a value defining the quality of encoding that will be passed
                to the encoder.
    kbs_steps:  a value defining the quality of encoding that will be displayed
                to the user. must be a one-to-one mapping with raw_steps.
    command:    the gstreamer pipeline to execute. should contain exactly one
                %s, which will be replaced with the value from raw_steps.
    plugins:    the gstreamer plugins needed for this transcode pipeline
    desc:       a description of the encoder to display to the user
"""

# NOTE: the transcoder is NOT designed to transfer tags. You will need to
# manually write the tags after transcoding has completed.


def get_formats():
    ret = {}
    for name, val in FORMATS.iteritems():
        try:
            for plug in val['plugins']:
                x = gst.element_factory_find(plug)
                if not x:
                    raise
            ret[name] = val
        except:
            pass
    return ret

def add_format(name, fmt):
    global FORMATS
    FORMATS[name] = fmt

class TranscodeError(Exception):
    pass

class Transcoder(object):
    def __init__(self, logbox_cb, formats):
        self.logbox_cb = logbox_cb
        #self.quality = 0.5
        self.sink = None
        self.dest_format = None
        self.encoder = None
        self.pipe = None
        self.bus = None
        self.running = False
        self.__last_time = 0.0
        self.FORMATS = formats
       

    def set_format(self, name):
        print "FORMAT = ", name
        self.dest_format = name

    def set_quality(self, value, FORMATS):
        if value in self.FORMATS[self.dest_format]['raw_steps']:
            self.quality = value
        else:
	  self.quality = self.FORMATS[self.dest_format]['default']

    def _construct_encoder(self):
        self.set_format(self.settings["outputFormat"])
        fmt = self.FORMATS[self.dest_format]
        quality = self.quality
        self.encoder = fmt["command"]%quality

    def set_input(self, uri):
        self.input = """filesrc location="%s" """%uri

    def set_raw_input(self, raw):
        self.input = raw

    def set_output(self, uri):
        self.output = """filesink location="%s" """%uri

    def set_output_raw(self, raw):
        self.output = raw

    def start_transcode(self, settings):
        self.settings = settings
        self._construct_encoder()
        self.currentTrack = self.output.split("/").pop().strip("\"")
        #self.logbox_cb("Transcoding %s" %self.currentTrack)
        if not os.path.exists(settings["outputDir"]): 
          os.mkdir(settings["outputDir"])
        
        elements = [ self.input, "decodebin name=\"decoder\"", "audioconvert",
                self.encoder, self.output ]
        pipestr = " ! ".join( elements )
        pipe = gst.parse_launch(pipestr)
        self.pipe = pipe
        self.bus = pipe.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)
        self.bus.connect('message::eos', self.on_eof)

        pipe.set_state(gst.STATE_PLAYING)
        self.running = True
        #self.runningCount += 1
        return pipe

    def stop(self):
        self.pipe.set_state(gst.STATE_NULL)
        self.running = False
        self.__last_time = 0.0
        self.logbox_cb("FINISHED: %s" %self.currentTrack)
        

    def on_error(self, *args):
        self.pipe.set_state(gst.STATE_NULL)
        self.running = False

    def on_eof(self, *args):
        self.stop()

    def get_time(self):
        if not self.running:
            return 0.0
        try:
            tim = self.pipe.query_position(gst.FORMAT_TIME)[0]
            tim = tim/gst.SECOND
            self.__last_time = tim
            return tim
        except:
            return self.__last_time

    def is_running(self):
        return self.running
