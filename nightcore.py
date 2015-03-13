# !/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from random import choice, random
from os import listdir


def speedup_audio(sound_array, factor):
    """
    Multiply the sound's speed by some factor (including pitch shift).
    source: http://goo.gl/MlI9UM
    """

    # Pick new indices with the factor as interval.
    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)

    # return a new array with just the data from the calculated indices.
    return sound_array[indices.astype(int)]


def dance_with_the_devil(sound_array, rate, glitches=0.25,
                         glitch_duration=1.00, volume=100):
    """
    Ruin the sound_array by adding random glitches, where the sound is sped up
    or slowed down. Also raise the volume.
    """

    # Create an array with all moments a glitch can occur.
    glitch_ops = np.arange(1, int(len(sound_array) / rate -
                           (glitch_duration * 2)), glitch_duration * 2)

    # Pick a fraction (the variable "glitches") of these opportunities
    np.random.shuffle(glitch_ops)
    splits = np.sort(glitch_ops[:int(len(glitch_ops) * glitches)])

    # Add the end of each glitch to the array and multiply with the rate so we
    # have the actual array indices.
    splits = np.insert(splits, np.arange(1, len(splits)),
                       np.array([s + glitch_duration for s in splits])) * rate

    # Split the audio so glitch pieces can be edited separately.
    pieces = np.split(sound_array, splits)

    # Speed up or slow down glitch pieces randomly.
    for i in np.arange(1, len(pieces), 2):
        pieces[i] = speedup_audio(pieces[i], random() * 1.5 + 0.5)

    # Put all pieces back together and multiply with volume.
    return np.concatenate(pieces) * volume


def prepare_audio(file_name, rate=44100, speedup=1.3, devil=False):
    """
    Read the audio from the input file, speed it up and return it as an
    AudioArrayClip.
    """

    # Create a new audio clip from file and write it to an array.
    audio = AudioFileClip(file_name)
    data = audio.to_soundarray(fps=rate)

    # Speedup the the data in the array and return it as an audio clip.
    data = speedup_audio(data, speedup)

    # If devil mode is enabled, dance, with the devil.
    if devil:
        data = dance_with_the_devil(data, rate)

    return AudioArrayClip(data, fps=rate)


def prepare_image(text, duration, fps=1):
    """
    Load a random image from file, add text to it and return it as aclip.
    """

    # Pick a random file from the images directory and load it into a clip.
    image_file = choice([file for file in listdir("images")])
    image = ImageClip("images/" + image_file).set_fps(fps)

    # Add the text on a transparent black ribbon.
    text = TextClip(txt=text, bg_color="rgba(0, 0, 0, 0.7)", color="white",
                    size=(1920, 150), font="Droid-Sans-Fallback")
    text = text.set_pos((0, 100))

    # Make a combined clip of the image and text clips, set its duration and
    # return it.
    return CompositeVideoClip([image, text]).set_duration(duration)


def nightcorify(source_file, destination_file, text, devil=False):
    """
    Create a nightcore video using the audio from source_file and write it to
    destination_file. Draw the text on top of the video.
    """

    # Read the audio from our source file.
    audio = prepare_audio(source_file, devil=devil)

    # Create a random image with the user text on it and set its duration to
    # the duration of the sped up audio.
    image = prepare_image(text, audio.duration)

    # Add the audio to this image clip and write the result to our destination
    # file.
    image.set_audio(audio).write_videofile(destination_file)


if __name__ == "__main__":
    from sys import argv, exit

    if len(argv) < 4:
        print "usage: nightcore.py <inputfile.wav> <outputfile.avi> " + \
              "<title> [-d]"
        exit(1)

    devil = (len(argv) > 4 and argv[4].lower() == "-d")
    nightcorify(argv[1], argv[2], argv[3], devil)
