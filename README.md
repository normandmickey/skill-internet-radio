## jarbas internet radio

Play internet radio station.


## Description

Play internet radio stations using Mycroft.

There is a folder named radios inside the skill that contains files with
"station name , station stream"  pairs

"metal.value"

    metal detector, http://ice1.somafm.com/metal-128-mp3
    death fm, http://death.fm/modules/Listen/MP3-hi.pls

each station in this name is associated to the file name and to each individual station name

    play metal radio -> chooses a random one from the list
    put some death fm music -> plays death fm
    listen to metal detector -> plays metal detector

if not direct match for a station is found stations are extracted from
utterance and fuzzy matched, adding new files should
enable the new station to be recognized by mycroft

# TODO get new stations from mycroft.home , this will be a list of keywords, streams


## Examples

* "internet radio"
* "web radio"
* "play some music"
* "rock radio"
* "play rock radio"
* "listen to rock radio"
* "country radio"
* "play country radio"
* "listen to country radio"
* "classical radio"
* "play classical radio"
* "listen to classical radio"
* "jazz radio"
* "play jazz radio"
* "listen to jazz radio"
* "top 40 radio"
* "play metal radio"
* "listen to favorite radio"
* "christmas radio"
* "play christmas radio"
* "listen to christmas radio"
* "psytube web radio"
* "drum and bass web radio"
* "techno radio"
* "minimal techno radio"
* "techno radio"
* "play goa psy trance"
* "listen to progressive psy trance"

## Credits

Jarbas AI
Norman Moore - [original inspiration](https://github.com/normandmickey/skill-internet-radio)
