#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import numpy as np
from scipy.io import wavfile

import Image
import ImageFont, ImageDraw
import moviepy.editor as mp
from moviepy.audio.AudioClip import AudioArrayClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from random import choice

FACTOR = 1.30
FPS = 1

# Text position
X = 50
Y = 50

# Text colors
FILLCOLOR = "white"
SHADOWCOLOR = "black"


def speedup_audio(sound_array, factor):
    """ Multiplies the sound's speed by some factor
        source: http://goo.gl/MlI9UM """

    indices = np.round(np.arange(0, len(sound_array), factor))
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[indices.astype(int)]


def prepare_image(text, v_id):
    """ Load the specified image from file, add text to it and save it in the
        folder for temporary files with its unique id as filename. """

    # Select an image at random from a library
    image_file = choice([file for file in os.listdir("./images")])

    image = Image.open("./images/" + image_file)

    # TODO: translate the text to japanese (or fake japanese?)
    draw = ImageDraw.Draw(image)
    # Use unicode for kanji support
    unicode_text = unicode(text)

    font = ImageFont.truetype('font.ttf', 48)

    # Fake a border around the text
    draw.text((X-2, Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X,   Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y-2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y  ), text, font=font, fill=SHADOWCOLOR)
    draw.text((X-2, Y  ), text, font=font, fill=SHADOWCOLOR)
    draw.text((X-2, Y+2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X,   Y+2), text, font=font, fill=SHADOWCOLOR)
    draw.text((X+2, Y+2), text, font=font, fill=SHADOWCOLOR)

    draw.text((X, Y), unicode_text, font=font, fill=FILLCOLOR)
    image.save("tmp/" + str(v_id) + ".png")


def prepare_audio(input_file, v_id, rate):
    """ Speed up the input sound and save it in the temporary folder using its
        unique video id as filename. """

    # rate, data = wavfile.read(input_file)
    audio = AudioFileClip(input_file)
    data = audio.to_soundarray(fps=rate)
    data = speedup_audio(data, FACTOR)
    # wavfile.write("tmp/" + str(v_id) + ".wav", rate, data)

    return rate, data


def build_video(id, image_file, sound_array, rate):
    """ Combine the new audio and image to make a nightcore video """

    # cmd = ('ffmpeg -loop 1 -r %s -i %s -i %s -shortest -acodec copy -f avi %s' %
    #     (FPS, "tmp/" + str(v_id) + ".png", "tmp/" + str(v_id) + ".wav", output_file))
    #
    # os.system(cmd)
    # print 'Video is complete, output written to %s' % output_file

    duration = len(sound_array) / float(rate)
    print duration
    image = mp.ImageClip("images/" + image_file, duration=duration)
    audio = AudioArrayClip(sound_array, fps=rate)
    text = TextClip(txt="Der holle rache", bg_color="rgba(0, 0, 0, 0.7)", color="white", size=(1920, 150), font="Droid-Sans-Fallback").set_duration(duration)
    text = text.set_pos((0, 100))
    # text.preview()
    # audio.preview()
    # audio = AudioFileClip("tmp/1.wav")

    # audio = mp.AudioClip(audio.make_frame)
    # video = mp.CompositeVideoClip([image, audio])
    # video.preview()

    video = (image.set_audio(audio)
                  .set_fps(1))
    video = CompositeVideoClip([video, text]).set_duration(duration)
    video.write_videofile("movie.mp4")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print "usage: nightcore.py <inputfile.wav> <outputfile.avi> <title>"
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    text = sys.argv[3]

    v_id = 1
    rate = 44100
    # v_id = generate_unique_id()

    # Prepare the image and audio. The files are saved to tmp/<unique id>
    # prepare_image(text, v_id)
    rate, sound_array = prepare_audio(input_file, v_id, rate)

    image_file = choice([file for file in os.listdir("./images")])

    build_video(v_id, image_file, sound_array, rate)
