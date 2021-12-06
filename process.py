import speech_recognition as sr 
import os 
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mp
import requests
import json
from modzy import ApiClient
from modzy._util import file_to_bytes
import pandas as pd


def video_to_audio(video):
    clip = mp.VideoFileClip(video)
    return clip.audio.write_audiofile(r"audio.wav")

def get_large_audio_transcription(path):
    
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return str(whole_text)


#Video Caption
def video_caption(video):
    client = ApiClient(base_url="https://app.modzy.com/api", api_key="LopsiSFjhQQ2WzoQmvLu.FsIykDCjSIHat5QgCSOc")
    sources = {}
    sources["my-input"] = {
        "input": video
    }
    job = client.jobs.submit_file("cyoxn54q5g", "0.0.2", sources)
    result = client.results.block_until_complete(job,timeout=None)
    return str(result['results']['my-input']['results.json']['caption'])

#Summary
def summary(transcript):
    client = ApiClient(base_url="https://app.modzy.com/api", api_key="LopsiSFjhQQ2WzoQmvLu.FsIykDCjSIHat5QgCSOc")
    sources = {}
    sources["my-input"] = {
        "input.txt": transcript
    }
    job = client.jobs.submit_text("rs2qqwbjwb", "0.0.2", sources)
    result = client.results.block_until_complete(job,timeout=None)
    a = result['results']['my-input']['results.json']['summary']
    return a

#Lookup Topic
def search_topics(word,audio):
    client = ApiClient(base_url="https://app.modzy.com/api", api_key="LopsiSFjhQQ2WzoQmvLu.FsIykDCjSIHat5QgCSOc")
    sources = {}
    sources["my-input"] = {
        "word.txt": file_to_bytes(word),
        "input.wav": file_to_bytes(audio)
    }
    job = client.jobs.submit_file("s25ge4ufw4", "0.0.1", sources)
    result = client.results.block_until_complete(job,timeout=None)
    a = result['results']['my-input']['results.json']
    return a

#Topics Covered
def topics_covered(transcript):
    client = ApiClient(base_url="https://app.modzy.com/api", api_key="LopsiSFjhQQ2WzoQmvLu.FsIykDCjSIHat5QgCSOc")
    sources = {}
    sources["my-input"] = {
        "input.txt": transcript
    }
    job = client.jobs.submit_text("m8z2mwe3pt", "0.0.1", sources)
    result = client.results.block_until_complete(job,timeout=None)
    a = result['results']['my-input']['results.json']
    return a

def database():
    result = []
    video_to_audio("vid.mp4")
    transcript = get_large_audio_transcription("audio.wav")
    summ = summary(transcript)
    imp_topics = topics_covered(transcript)
    words = search_topics("word.txt","audio.wav")
    caption = video_caption("vid.mp4")

    result.append(transcript)
    result.append(summ)
    result.append(imp_topics)
    result.append(words)
    result.append(caption)

    data = pd.DataFrame(result)
    data.to_csv("data.csv")

database()
    
        

