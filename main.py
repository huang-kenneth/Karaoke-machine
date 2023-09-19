from pytube import YouTube
from pydub import AudioSegment
import os
import sys
import subprocess
import shutil

# Download and separate track into vocals and instrumental
def YouTubeDownload(link):
    # importing packages
    from pytube import YouTube
    import os
    
    # url input from user
    yt = YouTube(link)
    
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    
    # check for destination to save file
    destination = "assets/video-downloads"

    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    base = base.replace(" ", "") # remove spaces
    new_file = base + '.mp3'

    print("Downloading audio from Youtube (Step 1 of 3)....................")
    # check if file exists
    if os.path.isfile(new_file):
        os.remove(out_file)
        print("File", new_file, "already exists")
    else:    
        os.rename(out_file, new_file)
        subprocess.run(["spleeter", "separate", "-p", "spleeter:2stems", "-o", "assets/split", str(new_file),],
                       stdout =subprocess.DEVNULL, stderr =subprocess.DEVNULL)
        print("File has been split successfully.")
        # result of success
    print(yt.title + " has been successfully downloaded.")
    return new_file # return the file name and path

def editFile(file_path):
    # convert to 16kHz and put in audio_converted folder
    file_name = os.path.basename(file_path) # ex. "cupid.mp3"
    file_name_no_ext = os.path.splitext(file_name)[0] # ex. "cupid"
    out_path = "assets/audio_converted/"
    subprocess.run(["ffmpeg", "-y", "-i", str(file_path), "-ar", "16000", "-acodec", "pcm_s16le", str(file_name_no_ext) + ".wav"], cwd = out_path,
                   stdout =subprocess.DEVNULL, stderr =subprocess.DEVNULL)
    #print(out_path + file_name)
    return file_name
    

def transcript_grabber(filename):
    #main.exe -m "ggml-model-whisper-base.en.bin" -f "vocals_edit.wav"
    if os.path.isfile("assets/audio_converted/" + str(filename) + ".wav.srt"):
        print("Transcript already exists, skipping transcript....................")
        return
    whisper_path = "SubsGen/whisper-bin-x64/"
    print("Generating transcript (Step 2 of 3)....................")
    subprocess.run([whisper_path + "main.exe", "-l", "auto", "-m", whisper_path + "ggml-medium.en.bin", "-f", "assets/audio_converted/" + str(filename) + ".wav", "-osrt"],
                   stdout =subprocess.DEVNULL, stderr =subprocess.DEVNULL)
    print("Transcript generated....................")

def video_maker(filename, include_vocals = False, vocals_volume_adj = 0):
    jpg = "assets/backgrounds/background.jpg"
    accompaniment = "assets/split/" + filename + "/accompaniment.wav"
    subtitles = "assets/audio_converted/" + filename + ".wav.srt"
    print("Making video (Step 3 of 3)....................")
    if include_vocals:
        # for editing vocals volume
        vocals = "assets/split/" + filename + "/vocals.wav" # NOT SURE TO USE THIS OR NOT. For now, setting as lower volume
        vocals_wav = AudioSegment.from_wav(vocals)
        vocals_wav = vocals_wav + vocals_volume_adj # adjust value by vocals_volume_adj
        accompaniment_wav = AudioSegment.from_wav(accompaniment)
        overlay = accompaniment_wav.overlay(vocals_wav)
        overlay.export("assets/split/" + filename + "/merged.wav", format='wav')
        merged = "assets/split/" + filename + "/merged.wav"

        # for adding to -vf 
        subprocess.run(["ffmpeg", "-loop", "1", "-y", 
                        "-i", jpg, "-i", merged,
                        "-shortest", 
                        "-vf", "subtitles=" + subtitles + ":force_style='Fontsize=24,Alignment=10',crop=trunc(iw/2)*2:trunc(ih/2)*2", 
                        "static/" + "output" + ".mp4"],
                        stdout =subprocess.DEVNULL, stderr =subprocess.DEVNULL)
    else:
        subprocess.run(["ffmpeg", "-loop", "1", "-y", 
                        "-i", jpg, "-i", accompaniment,
                        "-shortest", 
                        "-vf", "subtitles=" + subtitles + ":force_style='Fontsize=24,Alignment=10',crop=trunc(iw/2)*2:trunc(ih/2)*2", 
                        "static/" + "output" + ".mp4"],
                        stdout =subprocess.DEVNULL, stderr =subprocess.DEVNULL)

def clear_folders():
    print("Clearing temporary files (Step 3 of 3)....................")
    shutil.rmtree('assets/audio_converted')
    shutil.rmtree('assets/split')
    shutil.rmtree('assets/video-downloads')
    os.mkdir('assets/audio_converted')
    os.mkdir('assets/split')
    os.mkdir('assets/video-downloads')

def clear_output():
    print("Clearing existing output (Step 0 of 3)....................")
    shutil.rmtree("static")
    os.mkdir("static")

def main(link, include_vocals):
    clear_output()
    file = YouTubeDownload(link) # ex. "cupid.mp3"
    filename = os.path.splitext(os.path.basename(file))[0]  # ex. "cupid"
    editFile(file)
    transcript_grabber(filename)
    video_maker(filename, include_vocals = include_vocals) # default: no vocals. to add vocals, add include_vocals = True
    clear_folders()
    return f"static/{filename}.mp4" # return the file name and path