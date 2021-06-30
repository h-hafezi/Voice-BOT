import os
from pydub import AudioSegment

# assign files
AudioSegment.converter = os.path.abspath('ffmpeg.exe')
AudioSegment.ffmpeg = os.path.abspath('ffmpeg.exe')
AudioSegment.ffprobe = os.path.abspath('ffprobe.exe')


def convert(input_file, output_file="converted.wav"):
    sound = AudioSegment.from_ogg(input_file)
    sound.export(output_file, format="wav")

