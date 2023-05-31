## Youtube to mp4 Lyric Generator
We create a lyric video and remove vocals - just like videos when we go karaokeing! 

We use OpenAI's Whisper to create our speech-to-text subtitles for our videos and use other libraries to process and create our final video. 

This project is ultimately part of a bigger project that aims to recreate a karaoke machine with improvements to the system. Generally, karaoke spots have a limited selection of songs - our code allows the user to generate their own karaoke/lyric video with just a Youtube link!

## Installation
To set up your environment, run:

```
conda create -n <environment-name> --file req.txt
```
  
From https://huggingface.co/ggerganov/whisper.cpp/tree/main, download "ggml-base.en.bin" and drop it into SubsGen/whisper-bin-x64. 
  
Note: to use other models, download a different model and change the code's input model. The default is "ggml-base.en.bin". 
    
## Example output
Instrumentals + Lyrics: 
https://github.com/huang-kenneth/Karaoke-machine/assets/67389462/362cd9ab-3096-479d-b7cd-e3a37b3d34c6

## To do (Mostly UI/Code Cleaning Changes):
  - Allow users to easily add or remove vocals when creating their song. Currently is a parameter in the code, will need to add a better UI.
  - Make selecting Whisper models easier for users. 
  - Better UI for where to paste the Youtube link.
  - Allow users to change the background of video. 
  - Follow words as song progresses (like karaoke videos)
  - Delete unneccesary files after done running.
  - Choose whether to overwrite or skip existing files. 
