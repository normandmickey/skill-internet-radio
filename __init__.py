# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill

try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None

from os.path import join
from os import listdir
import random
import csv
import subprocess
from mycroft.util.parse import fuzzy_match


__author__ = 'jarbas'


class InternetRadioSkill(MycroftSkill):
    def __init__(self):
        super(InternetRadioSkill, self).__init__()
        self.audioservice = None
        self.process = None

    def initialize(self):
        if "stations" not in self.settings:
            self.settings["stations"] = {"favorite": ["http://somafm.com/groovesalad.pls"]}
        if "station_files" not in self.settings:
            self.settings["station_files"] = join(self.root_dir, "radios")
        if "min_score" not in self.settings:
            self.settings["min_score"] = 0.3

        self.get_stations()

        intent = IntentBuilder("InternetRadioIntent") \
            .optionally("PlayKeyword") \
            .require("InternetRadioKeyword").build()

        self.register_intent(intent, self.handle_intent)

        intent = IntentBuilder("RandomInternetRadioIntent") \
            .optionally("PlayKeyword") \
            .require("InternetRadioKeyword").require("RandomKeyword").build()

        self.register_intent(intent, self.handle_random_intent)

        intent = IntentBuilder("InternetRadioStationIntent") \
            .require("InternetRadioStation")\
            .one_of("PlayKeyword", "InternetRadioKeyword").build()

        self.register_intent(intent, self.handle_station_intent)

        if AudioService:
            self.audioservice = AudioService(self.emitter)

        self.check_vlc()

    def get_stations(self):
        # TODO read remote config stations

        # read configured radio stations
        styles = listdir(self.settings.get("station_files"))

        stations = {}
        for style in styles:
            style = style.replace(".value", "")
            stations[style] = []
            result = self.translate_namedradios(style)
            for station in result:
                station = station.rstrip().lstrip()
                stations[station] = [result[station]]
                stations[style].append(result[station])

        # merge into settings
        for station in stations:
            # do not overwrite any that is already in settings
            if station not in self.settings["stations"].keys():
                self.settings["stations"][station] = stations[station]

        # create vocabulary
        for station in self.settings["stations"].keys():
            self.register_vocabulary(station, "InternetRadioStation")

    def handle_intent(self, message):
        # guess if some station was requested
        utterance = message.utterance_remainder()
        self.log.info("remainder: " + utterance)
        best_score = 0.0
        best_station = "favorite"
        if len(utterance):
            for station in self.settings["stations"].keys():
                score = fuzzy_match(station, utterance)
                self.log.info(str(score) + " " + station)
                if best_score < self.settings.get("min_score", 0.5):
                    continue
                if score > best_score:
                    best_station = station
                elif score == best_score:
                    # chose the smallest name
                    best_station = best_station if len(best_station) < len(
                        station) else station

        tracks = self.settings["stations"][best_station]
        if not self.play_track(tracks, best_station):
            self.speak_dialog("invalid.track", {"station": best_station})

    def handle_random_intent(self, message):
        # choose a random track for this station/style name
        best_station = random.choice(self.settings["stations"].keys())
        tracks = self.settings["stations"][best_station]
        if not self.play_track(tracks, best_station):
            self.speak_dialog("invalid.track", {"station": best_station})

    def handle_station_intent(self, message):
        best_station = message.data.get("InternetRadioStation")
        tracks = self.settings["stations"][best_station]
        if not self.play_track(tracks, best_station):
            self.speak_dialog("invalid.track", {"station": best_station})

    def play_track(self, tracks, name=""):
        if not isinstance(tracks, list):
            tracks = [tracks]
        if not len(tracks):
            return False
        track = random.choice(tracks)
        if not self.check_track_support(track):
            tracks = [track for track in tracks if ".pls" not in track]
            if len(tracks):
                track = random.choice(tracks)
            else:
                return False
        # Display icon on faceplate
        self.enclosure.deactivate_mouth_events()
        # music code
        png = "IIAEAOOHGAGEGOOHAA"

        self.enclosure.mouth_display(png,  x=10, y=0,
                                         refresh=True)

        if self.audioservice:
            if self.audioservice.is_playing:
                self.audioservice.stop()
            self.audioservice.play(track, utterance="vlc")
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(track)

        return True

    def translate_namedradios(self, name, delim=None):
        delim = delim or ','
        result = {}
        if not name.endswith(".value"):
            name += ".value"

        try:
            with open(join(self.settings["station_files"], name)) as f:
                reader = csv.reader(f, delimiter=delim)
                for row in reader:
                    # skip blank or comment lines
                    if not row or row[0].startswith("#"):
                        continue
                    if len(row) != 2:
                        continue
                    if row[0] not in result.keys():
                        result[row[0].rstrip().lstrip()] = []
                    result[row[0]].append(row[1].rstrip().lstrip())
            return result
        except Exception as e:
            self.log.error(e)
            return {}

    def check_track_support(self, track):
        if ".pls" in track:
            if AudioService is None:
                return False
            elif not self.vlc_installed():
                return False
        return True

    def check_vlc(self):
        if AudioService is None:
            self.speak_dialog("audio.missing")
            return False
        elif not self.vlc_installed():
            self.speak_dialog("vlc.missing")
            return False
        return True

    def vlc_installed(self):
        # TODO fix me
        return True
        try:
            vlc = subprocess.check_output('dpkg -l vlc')
        except Exception as e:
            self.log.warning(e)
            return False
        if "no packages found matching" in vlc:
            return False
        return True

    def stop(self):
        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()
        if self.audioservice:
            if self.audioservice.is_playing:
                self.audioservice.stop()
        else:
            if self.process and self.process.poll() is None:
                self.process.terminate()
                self.process.wait()


def create_skill():
    return InternetRadioSkill()
