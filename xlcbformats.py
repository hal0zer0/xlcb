# -*- coding: utf-8 -*-
from xl.nls import gettext as _

def get_formats():
    FORMATS = {
        "Ogg Vorbis" : {
            "default"   : 0.5,
            "raw_steps" : [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            "kbs_steps" : [64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
            "command"   : "vorbisenc quality=%s ! oggmux",
            "extension" : "ogg",
            "plugins"   : ["vorbisenc", "oggmux"],
            "desc"      : _("Vorbis is an open source, lossy audio codec with "
                    "high quality output at a lower file size than MP3.")
            },
        "FLAC" : {
            "default"   : 5,
            "raw_steps" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "kbs_steps" : [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            "command"   : "flacenc quality=%s",
            "extension" : "flac",
            "plugins"   : ["flacenc"],
            "desc"      : _("Free Lossless Audio Codec (FLAC) is an open "
                    "source codec that compresses but does not degrade audio "
                    "quality.")
            },
        "AAC"       : {
            "default"   : 160000,
            "raw_steps" : [32000, 48000, 64000, 96000, 128000, 160000,
                    192000, 224000, 256000, 320000],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "faac bitrate=%s ! ffmux_mp4",
            "extension" : "m4a",
            "plugins"   : ["faac", "ffmux_mp4"],
            "desc"      : _("Apple's proprietary lossy audio format that "
                    "achieves better sound quality than MP3 at "
                    "lower bitrates.")
            },
        "MP3 (VBR)" : {
            "default"   : 160,
            "raw_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "lame vbr=4 vbr-mean-bitrate=%s",
            "extension" : "mp3",
            "plugins"   : ["lame"],
            "desc"      : _("A proprietary and older, but also popular, lossy "
                    "audio format. VBR gives higher quality than CBR, but may "
                    "be incompatible with some players.")
            },
        "MP3 (CBR)" : {
            "default"   : 160,
            "raw_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "kbs_steps" : [32, 48, 64, 96, 128, 160, 192, 224, 256, 320],
            "command"   : "lame bitrate=%s",
            "extension" : "mp3",
            "plugins"   : ["lame"],
            "desc"      : _("A proprietary and older, but also popular, "
                    "lossy audio format. CBR gives less quality than VBR, "
                    "but is compatible with any player.")
            },
        "WavPack" : {
            "default"   : 2,
            "raw_steps" : [1,2,3,4],
            "kbs_steps" : [1,2,3,4],
            "command"   : "wavpackenc mode=%s",
            "extension" : "wv",
            "plugins"   : ["wavpackenc"],
            "desc"      : _("A very fast Free lossless audio format with "
                    "good compression."),
            },
        }
    return FORMATS