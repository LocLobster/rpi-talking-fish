#!/usr/bin/python3
import body_motor_controller
import audio_detector
import enum
import time
import queue

class AudioType(enum.Enum):
    SPEECH = enum.auto()
    SONG   = enum.auto()

class FishController():
    def __init__(self):
        self.audio_type = AudioType.SPEECH
        self.timer = 0.0
        self.audio_detector_sleep_time = 0.25
        self.mc = body_motor_controller.BodyMotorController()
        self.command_queue = queue.Queue()
        self.response_queue = queue.Queue()

    def start(self):
        while(True):
            if not self.command_queue.empty():
                command = self.command_queue.get()
                self.process_command(command)
                self.response_queue.put(1)

            result = audio_detector.check_audio_playing()
            if result:
                if self.audio_type == AudioType.SPEECH:
                    self.move_fish_speech()
                elif self.audio_type == AudioType.SONG:
                    self.move_fish_song()

            time.sleep(self.audio_detector_sleep_time)

    def set_queues(self, command_queue, response_queue):
        self.command_queue = command_queue
        self.response_queue = response_queue

    def set_expected_audio(self, audio_type):
        if audio_type == "song":
            self.audio_type = AudioType.SONG
        else:
            self.audio_type = AudioType.SPEECH

    def process_command(self, command):
        if command == "song":
            self.audio_type = AudioType.SONG
        elif command == "speech":
            self.audio_type = AudioType.SPEECH

    def move_fish_speech(self):
        audio_playing = True    
        self.mc.head_out()
        while audio_playing: 
            time.sleep(.2)
            audio_playing = audio_detector.check_audio_playing()
        self.mc.all_stop()

    def move_fish_song(self):
        audio_playing = True    
        while audio_playing: 
            audio_playing = audio_detector.check_audio_playing()
            self.flap_tail(.2)
            time.sleep(.36)

        self.mc.all_stop()
        self.timer = 0.0

    def flap_tail(self, duration=0.2):
        self.mc.tail_out()
        time.sleep(duration)
        self.mc.tail_stop()

class FishThread():
    def __init__(self, command_queue, response_queue):
        self.command_queue = command_queue
        self.response_queue = response_queue 

    def start(self):
        fish = FishController()
        fish.set_queues(self.command_queue, self.response_queue)
        fish.start()


if __name__ == '__main__':
    q1 = queue.Queue()
    q2 = queue.Queue()
    fish_thread = FishThread(q1, q2)
    fish_thread.start()
