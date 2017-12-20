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
import re

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

        intent = IntentBuilder("ChildrensRadioIntent").require(
             "ChildrensRadioKeyword").build()
        self.register_intent(intent, self.handle_childrens_intent)

        intent = IntentBuilder("InternetRadioStopIntent") \
                .require("InternetRadioStopVerb") \
                .require("InternetRadioKeyword").build()
        self.register_intent(intent, self.handle_stop)
   
        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_intent(self, message):
           self.stop()
           self.speak_dialog('internet.radio')
           time.sleep(4)

           if self.audioservice:
               self.audioservice.play(self.settings['station_url'])
           else: # othervice use normal mp3 playback
               self.process = play_mp3(self.settings['station_url'])

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
