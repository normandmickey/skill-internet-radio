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

station = 'http://144.217.253.136:8564/stream'

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


class PlaySomeMusicSkill(MycroftSkill):
    def __init__(self):
        super(PlaySomeMusicSkill, self).__init__(name="PlaySomeMusicSkill")
        self.audioservice = None

    def initialize(self):
        play_some_music_intent = IntentBuilder("PlaySomeMusicIntent"). \
            require("PlaySomeMusicKeyword").build()
        self.register_intent(play_some_music_intent,
                             self.handle_play_some_music_intent)
   
        if AudioService:
            self.audioservice = AudioService(self.emitter)

    def handle_play_some_music_intent(self, message):
        self.stop()
        self.speak_dialog("play.some.music")

        if self.audioservice:
                self.audioservice.play(station)
        else: # othervice use normal mp3 playback
                self.process = play_mp3(station)

    def stop(self):
        pass


def create_skill():
    return PlaySomeMusicSkill()
