import os
import openai
from pydub import AudioSegment
AudioSegment.converter = r"C:/PATH_Programs/ffmpeg.exe"
AudioSegment.ffmpeg = r"C:/PATH_Programs/ffmpeg.exe"
AudioSegment.ffprobe = r"C:/PATH_Programs/ffprobe.exe"

import math
openai.api_key = os.getenv("OPENAI_API_KEY")

def split_audio(file_path, chunk_size):
    audio = AudioSegment.from_file(file_path)
    length_audio = math.ceil(audio.duration_seconds)
    chunks = list()

    for i in range(0, length_audio, chunk_size):
        start_time = i * 1000  # start_time in milliseconds
        end_time = (i + chunk_size) * 1000  # end_time in milliseconds

        # create a chunk
        chunk = audio[start_time:end_time]
        chunks.append(chunk)

    return chunks

# split audio file into 30-second chunks (or adjust to your need)
chunks = split_audio("C:/Users/aliva/Desktop/AiO/OpenAI/utAustinRecording.mp3", 200)

# save each chunk to a file
for i, chunk in enumerate(chunks):
    chunk.export(f"chunk{i}.wav", format="wav")

file_names = [f"chunk{i}.wav" for i in range(len(chunks))]

for file_name in file_names:
    audio = open(file_name, 'rb')
    transcript = openai.Audio.transcribe("whisper-1", audio)
    print(transcript)
