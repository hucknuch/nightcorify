#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np

from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from random import choice
from os import listdir


def speedup_audio(sound_array, factor):
    """ Multiplies the sound's speed by some factor
        source: http://goo.gl/MlI9UM """

    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices.astype(int)]


def prepare_audio(input_file, rate=44100, speedup=1.3):
    """ Read the audio from the input file, speed it up and return it as an
        AudioArrayClip. """

    audio = AudioFileClip(input_file)
    data = audio.to_soundarray(fps=rate)
    data = speedup_audio(data, speedup)

    return AudioArrayClip(data, fps=rate)


def prepare_image(text, duration, fps=1):
    """ Load a random image from file, add text to it and return it as a
        clip. """

    image_file = choice([file for file in listdir("./images")])
    image = ImageClip("./images/" + image_file).set_fps(fps)
    text = TextClip(txt=text, bg_color="rgba(0, 0, 0, 0.7)", color="white",
                    size=(1920, 150), font="Droid-Sans-Fallback")

    text = text.set_pos((0, 100))

    return CompositeVideoClip([image, text]).set_duration(duration)


def nightcorify(source_file, destination_file, text):
    """ Create a nightcore video using the audio from source_file and write it
        to destination_file. Draw the text on top of the video. """

    audio = prepare_audio(source_file)
    image = prepare_image(text, audio.duration)
    video = image.set_audio(audio)

    video.write_videofile(destination_file)


if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) < 4:
        print "usage: nightcore.py <inputfile.wav> <outputfile.avi> <title>"
        exit(1)

    nightcorify(argv[1], argv[2], argv[3])
