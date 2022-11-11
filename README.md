# rpi-talking-fish
![Main Form Display](https://github.com/LocLobster/rpi-talking-fish/blob/master/fish_site.png)

An implementation of the infamous Billy Bass talking fish hack that I made for my kid's trunk or treat. I wanted to have text to speech to interact with the trick-or-treaters.
I couldn't find what I wanted from existing Billy Bass repos. Most of them fed an audio signal to an ardiuno/microcontroller that controlled the motors. I wanted to have a audio originate inside the fish and have a web interface. 

This repo was developed for a raspberry pi 3B+. The pi drives the fish's three motors using two L298N H-Bridges. Audio goes out from the rpi to an external speaker. A web interface is used to control the fish which has text to speech, random fish facts, and a way to start playing a song.

There are two "talking modes" for the fish.  In 'speech' mode, the head moves out and the the mouth moves with the audio.  In 'song' mode, the tail moves out and in to simulate a song's beat.  The timing is hard-coded. 
The mouth movement uses cava, a console audio visualizer/EQ.  The data from cava is piped to a python application which looks at the amplitude of an audio band.  

This was a fun project and I hope someone makes some use of it. I could write a tutorial but I'm rather lazy and Halloween is over now.  If you have questions, open an issue. I'd be happy to help. 
