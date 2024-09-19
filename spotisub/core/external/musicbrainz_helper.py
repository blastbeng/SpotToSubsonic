# loading in modules
import os
import time

from dotenv import load_dotenv
from os.path import dirname
from os.path import join
from spotdl import Spotdl
from spotdl.types.options import DownloaderOptions
from spotdl.types.song import Song
from .constants import constants
from .utils import utils
import musicbrainzngs
import logging

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


# Disabling musicbrainz INFO log as we don't want to see ugly infos in the
# console
log = logging.getLogger("musicbrainzngs")
log.setLevel(40)

musicbrainzngs.set_useragent(
    "navidrome music",
    "0.1",
    "http://example.com/music")


def get_isrc_by_id(song):
    try:
        if "musicBrainzId" in song and song["musicBrainzId"] is not None and song["musicBrainzId"] != "":
            song = musicbrainzngs.get_recording_by_id(
                song["musicBrainzId"], includes=["isrcs"])
            time.sleep(1)
            if (song is not None and "recording" in song
                and song["recording"] is not None and "isrc-list" in song["recording"]
                    and song["recording"]["isrc-list"] is not None and len(song["recording"]["isrc-list"])) > 0:
                return song["recording"]["isrc-list"]
        return []
    except BaseException:
        utils.write_exception()
        return []
