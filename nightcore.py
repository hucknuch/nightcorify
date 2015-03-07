# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from random import choice
from os import listdir


def speedup_audio(sound_array, factor):
    """
    Multiplies the sound's speed by some factor (including pitch shift).
    source: http://goo.gl/MlI9UM
    """

    # Pick new indices with the factor as interval
    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)

    # return a new array with just the data from the calculated indices
    return sound_array[indices.astype(int)]


def prepare_audio(file_name, rate=44100, speedup=1.3):
    """
    Read the audio from the input file, speed it up and return it as an
    AudioArrayClip.
    """

    # Create a new audio clip from file and write is to an array.
    audio = AudioFileClip(file_name)
    data = audio.to_soundarray(fps=rate)

    # Speedup the the data in the array and return it as an audio clip.
    return AudioArrayClip(speedup_audio(data, speedup), fps=rate)


def prepare_image(text, duration, fps=1):
    """
    Load a random image from file, add text to it and return it as aclip.
    """

    # Pick a random file from the images directory and load it into a clip.
    image_file = choice([file for file in listdir("./images")])
    image = ImageClip("images/" + image_file).set_fps(fps)

    # Add the text on a transparent black ribbon.
    text = TextClip(txt=text, bg_color="rgba(0, 0, 0, 0.7)", color="white",
                    size=(1920, 150), font="Droid-Sans-Fallback")
    text = text.set_pos((0, 100))

    # Make a combined clip of the image and text clips, set its duration and
    # return it.
    return CompositeVideoClip([image, text]).set_duration(duration)


def nightcorify(source_file, destination_file, text):
    """
    Create a nightcore video using the audio from source_file and write it to
    destination_file. Draw the text on top of the video.
    """

    # Read the audio from our source file.
    audio = prepare_audio(source_file)

    # Create a random image with the user text on it and set its duration to
    # the duration of the sped up audio.
    image = prepare_image(text, audio.duration)

    # Add the audio to this image clip and write the result to our destination
    # file.
    image.set_audio(audio).write_videofile(destination_file)


if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) < 4:
        print "usage: nightcore.py <inputfile.wav> <outputfile.avi> <title>"
        exit(1)

    nightcorify(argv[1], argv[2], argv[3])
