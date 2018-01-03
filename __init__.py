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

import time
import requests
import random
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
try:
    from mycroft.skills.audioservice import AudioService
except:
    from mycroft.util import play_mp3
    AudioService = None

__author__ = 'nmoore'


LOGGER = getLogger(__name__)


class InternetRadioSkill(MycroftSkill):
    def __init__(self):
        super(InternetRadioSkill, self).__init__(name="InternetRadioSkill")
        self.audioservice = None
        self.process = None

    def initialize(self):
        intent = IntentBuilder("InternetRadioIntent").require(
             "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_intent)

        intent = IntentBuilder("HarkIntent").require(
             "HarkKeyword").require("RadioSearch").build()
        self.register_intent(intent, self.handle_hark_intent)

        intent = IntentBuilder("CountryRadioIntent").require(
             "CountryRadioKeyword").build()
        self.register_intent(intent, self.handle_country_intent)

        intent = IntentBuilder("RockRadioIntent").require(
             "RockRadioKeyword").build()
        self.register_intent(intent, self.handle_rock_intent)

        intent = IntentBuilder("ClassicalRadioIntent").require(
             "ClassicalRadioKeyword").build()
        self.register_intent(intent, self.handle_classical_intent)

        intent = IntentBuilder("Top40RadioIntent").require(
             "Top40RadioKeyword").build()
        self.register_intent(intent, self.handle_top40_intent)

        intent = IntentBuilder("JazzRadioIntent").require(
             "JazzRadioKeyword").build()
        self.register_intent(intent, self.handle_jazz_intent)

        intent = IntentBuilder("ChristmasRadioIntent").require(
             "ChristmasRadioKeyword").build()
        self.register_intent(intent, self.handle_christmas_intent)

        intent = IntentBuilder("FavoriteRadioIntent").require(
             "FavoriteRadioKeyword").build()
        self.register_intent(intent, self.handle_favorite_intent)

        intent = IntentBuilder("ChildrensRadioIntent").require(
             "ChildrensRadioKeyword").build()
        self.register_intent(intent, self.handle_childrens_intent)

        intent = IntentBuilder("InternetRadioStopIntent") \
                .require("InternetRadioStopVerb") \
                .require("InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_stop)

        intent = IntentBuilder("DarkPsyRadioIntent").require(
            "DarkKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_dark_psy_intent)

        intent = IntentBuilder("DarkProgressivePsyRadioIntent").require(
            "DarkKeyword").require("ProgressiveKeyword").require(
            "PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_dark_prog_psy_intent)

        intent = IntentBuilder("ProgressivePsyRadioIntent").require("ProgressiveKeyword").require(
            "PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_prog_psy_intent)

        intent = IntentBuilder("FullonPsyRadioIntent").require(
            "FullOnKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_fullon_intent)

        intent = IntentBuilder("GoaPsyRadioIntent").require(
            "GoaKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_goa_intent)

        intent = IntentBuilder("ForestPsyRadioIntent").require(
            "ForestKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_forest_intent)

        intent = IntentBuilder("SuomiPsyRadioIntent").require(
            "SuomiKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_suomi_intent)

        intent = IntentBuilder("HitechCorePsyRadioIntent").require(
            "HiTechKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_hitech_psy_intent)

        intent = IntentBuilder("OrochillPsyRadioIntent").require(
            "OrochillKeyword").require("PsytubeKeyword").optionally(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_orochill_intent)

        intent = IntentBuilder("TechnoRadioIntent").require(
            "TechnoRadioKeyword").optionally("PsytubeKeyword").require(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_techno_intent)

        intent = IntentBuilder("MinimalTechnoRadioIntent").require(
            "MinimalTechnoRadioKeyword").optionally(
            "PsytubeKeyword").require(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_minimal_techno_intent)

        intent = IntentBuilder("DNBRadioIntent").require(
            "DrumNBassRadioKeyword").optionally(
            "PsytubeKeyword").require(
            "InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_dnb_intent)

        intent = IntentBuilder("PsytubeInternetRadioIntent").require(
            "InternetRadioKeyword").require(
            "PsytubeKeyword").build()
        self.register_intent(intent, self.handle_psytube_intent)

        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_psytube_intent(self, message):
        self.stop()
        self.speak_dialog('psytube')
        time.sleep(4)
        urls = ["dark_psy_trance_station_url",
                "progressive_psy_trance_station_url",
                "dark_progressive_psy_trance_station_url",
                "forest_psy_trance_station_url",
                "suomi_psy_trance_station_url",
                "fullon_psy_trance_station_url",
                "goa_psy_trance_station_url"]
        if self.audioservice:
            self.audioservice.play(random.choice(urls))
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(random.choice(urls))

    def handle_hitech_psy_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'hitech_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'hitech_psy_trance_station_url'])

    def handle_dark_psy_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'dark_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'dark_psy_trance_station_url'])

    def handle_dark_prog_psy_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'dark_progressive_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'dark_progressive_psy_trance_station_url'])

    def handle_prog_psy_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'progressive_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'progressive_psy_trance_station_url'])

    def handle_fullon_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'fullon_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'fullon_psy_trance_station_url'])

    def handle_goa_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'goa_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'goa_psy_trance_station_url'])

    def handle_forest_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings[
                                       'forest_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings[
                                        'forest_psy_trance_station_url'])

    def handle_suomi_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings['suomi_psy_trance_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings['suomi_psy_trance_station_url'])

    def handle_orochill_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings['orochill_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings['orochill_station_url'])

    def handle_techno_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings['techno_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings['techno_station_url'])

    def handle_minimal_techno_intent(self, message):
        self.stop()
        self.speak_dialog('internet.radio')
        time.sleep(4)

        if self.audioservice:
            self.audioservice.play(self.settings['minimal_techno_station_url'])
        else:  # othervice use normal mp3 playback
            self.process = play_mp3(self.settings['minimal_techno_station_url'])

    def handle_dnb_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['drumnbass_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['drumnbass_station_url'])

    def handle_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)
           search_string = message.data.get('RadioSearch')

           if self.audioservice:
               self.audioservice.play(self.settings['station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['station_url'])

    def handle_hark_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)
           search_string = message.data.get('RadioSearch')
           s_details = requests.get('http://greatesthits.rocks:5000/station')
           stations = s_details.json()
           stream_url2 = 'none'
           for station in stations:
               if (search_string).lower() == station['name'].lower():
                  stream_url = station['url']
                  stream_url2 = stream_url.encode('utf-8')
                  self.audioservice.play(stream_url2)
                  break

    def handle_country_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['country_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['country_station_url'])

    def handle_rock_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['rock_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['rock_station_url'])
    
    def handle_classical_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['classical_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['classical_station_url'])

    def handle_top40_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['top40_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['top40_station_url'])

    def handle_jazz_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['jazz_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['jazz_station_url'])

    def handle_christmas_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['christmas_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['christmas_station_url'])

    def handle_favorite_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['favorite_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['favorite_station_url'])
             
    def handle_childrens_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['childrens_station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['childrens_station_url'])
             
    def handle_stop(self, message):
        self.stop()
        self.speak_dialog('internet.radio.stop')

    def stop(self):
        if self.audioservice:
           self.audioservice.stop()
        else:
            if self.process and self.process.poll() is None:
               self.process.terminate()
               self.process.wait()

def create_skill():
    return InternetRadioSkill()
