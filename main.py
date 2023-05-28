from pytube import YouTube
from pydub import AudioSegment
import os
import sys
import subprocess

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
    new_file = base + '.mp3'

    # check if file exists
    if os.path.isfile(new_file):
        os.remove(out_file)
        print("File", new_file, "already exists")
    else:    
        os.rename(out_file, new_file)
        subprocess.run(["spleeter", "separate", "-p", "spleeter:2stems", "-o", "assets/split", str(new_file)])
        # result of success
    print(yt.title + " has been successfully downloaded.")
    return new_file # return the file name and path

def editFile(file_path):
    # convert to 16kHz and put in audio_converted folder
    file_name = os.path.basename(file_path) # ex. "cupid.mp3"
    file_name_no_ext = os.path.splitext(file_name)[0] # ex. "cupid"
    out_path = "assets/audio_converted/"
    subprocess.run(["ffmpeg", "-y", "-i", str(file_path), "-ar", "16000", "-acodec", "pcm_s16le", str(file_name_no_ext) + ".wav"], cwd = out_path)
    print(out_path + file_name)
    return file_name
    

def transcript_grabber(filename):
    #main.exe -m "ggml-model-whisper-base.en.bin" -f "vocals_edit.wav"
    if os.path.isfile("assets/audio_converted/" + str(filename) + ".wav.srt"):
        print("Transcript already exists, skipping transcript....................")
        return
    whisper_path = "SubsGen/whisper-bin-x64/"
    subprocess.run([whisper_path + "main.exe", "-l", "auto", "-m", whisper_path + "ggml-medium.en.bin", "-f", "assets/audio_converted/" + str(filename) + ".wav", "-osrt"])
    print("Transcript generated....................")

def video_maker(filename, include_vocals = False, vocals_volume_adj = 0):
    jpg = "assets/backgrounds/background.jpg"
    accompaniment = "assets/split/" + filename + "/accompaniment.wav"
    subtitles = "assets/audio_converted/" + filename + ".wav.srt"

    if include_vocals:
        # for editing vocals volume
        vocals = "assets/split/" + filename + "/vocals.wav" # NOT SURE TO USE THIS OR NOT. For now, setting as lower volume
        vocals_wav = AudioSegment.from_wav(vocals)
        vocals_wav = vocals_wav + vocals_volume_adj # lower volume by 20 dB
        accompaniment_wav = AudioSegment.from_wav(accompaniment)
        overlay = accompaniment_wav.overlay(vocals_wav)
        overlay.export("assets/split/" + filename + "/merged.wav", format='wav')
        merged = "assets/split/" + filename + "/merged.wav"

        # for adding to -vf 
        subprocess.run(["ffmpeg", "-loop", "1", "-y", 
                        "-i", jpg, "-i", merged,
                        "-shortest", 
                        "-vf", "subtitles=" + subtitles + ":force_style='Fontsize=24,Alignment=10',crop=trunc(iw/2)*2:trunc(ih/2)*2", 
                        "assets/output/" + filename + ".mp4"])
    else:
        subprocess.run(["ffmpeg", "-loop", "1", "-y", 
                        "-i", jpg, "-i", accompaniment,
                        "-shortest", 
                        "-vf", "subtitles=" + subtitles + ":force_style='Fontsize=24,Alignment=10',crop=trunc(iw/2)*2:trunc(ih/2)*2", 
                        "assets/output/" + filename + ".mp4"])

def main():
    link = "https://www.youtube.com/watch?v=2ggzxInyzVE"
    file = YouTubeDownload(link) # ex. "cupid.mp3"
    filename = os.path.splitext(os.path.basename(file))[0]  # ex. "cupid"
    editFile(file)
    transcript_grabber(filename)
    video_maker(filename) # default: no vocals. to add vocals, add include_vocals = True

if __name__ == "__main__":
    main()
    # to add: 
    # option: delete all files in assets folder after done
    # option: choose whether to overwrite existing files
    # option: follow which word we're on 
