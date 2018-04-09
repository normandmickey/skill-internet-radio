from adapt.intent import IntentBuilder
from mycroft.skills.core import intent_handler

from os.path import join, dirname
from os import listdir
import random
import csv
from mycroft.util.parse import match_one, normalize
from mycroft_jarbas_utils.skills.audio import AudioSkill


__author__ = 'jarbas'


class InternetRadioSkill(AudioSkill):
    def __init__(self):
        super(InternetRadioSkill, self).__init__()
        self.stations = {}
        if "station_files" not in self.settings:
            self.settings["station_files"] = join(dirname(__file__), "radios")
        if "min_score" not in self.settings:
            self.settings["min_score"] = 0.4

    def translate_named_radios(self, name, delim=None):
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
            self.log.error(str(e))
            return {}

    def get_stations_from_file(self):
        # read configured radio stations
        styles = listdir(self.settings["station_files"])
        for style in styles:
            self.log.info("loading radio stations from: " + style)
            name = style.replace(".value", "")
            if name not in self.stations:
                self.stations[name] = []
            style_stations = self.translate_named_radios(style)
            for station_name in style_stations:
                self.log.info("loading station: " + station_name)
                if station_name not in self.stations:
                    self.stations[station_name] = []
                else:
                    for s in style_stations[station_name]:
                        if s not in self.stations[station_name]:
                            self.log.info("adding url: " + s)
                            self.stations[station_name].append(s)
                for s in style_stations[station_name]:
                    if s not in self.stations[name]:
                        self.log.info("adding url: " + s)
                        self.stations[name].append(s)

    @intent_handler(IntentBuilder("InternetRadioIntent")
                    .optionally("PlayKeyword")
                    .require("InternetRadioKeyword"))
    def handle_radio_intent(self, message):
        # guess if some station was requested
        utterance = normalize(message.utterance_remainder(), self.lang)
        self.log.info("remainder: " + utterance)
        best_station = "favorite"
        if utterance:
            best_station = match_one(utterance, self.stations.keys())

        tracks = random.shuffle(self.stations[best_station])
        self.log.info("Now playing: " + str(tracks))
        if not self.play_track(tracks, best_station):
            self.speak_dialog("invalid.track", {"station": best_station})

    @intent_handler(IntentBuilder("RandomInternetRadioIntent")
                    .optionally("PlayKeyword")
                    .require("InternetRadioKeyword")
                    .require("RandomKeyword"))
    def handle_random_intent(self, message):
        # choose a random track for this station/style name
        best_station = random.choice(self.stations.keys())
        tracks = self.stations[best_station]
        if not self.play_track(tracks, best_station):
            self.speak_dialog("invalid.track", {"station": best_station})

    def play_track(self, tracks, name=""):
        if not isinstance(tracks, list):
            tracks = [tracks]
        if not len(tracks):
            return False

        self.speak_dialog("internet.radio", {"station": name})
        self.play(tracks)
        return True


def create_skill():
    return InternetRadioSkill()
