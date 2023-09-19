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

After setup, enter the virtual environment and run:
```
python app.py
```

You should see a homepage after going to the given url in the console (ex. http://127.0.0.1:5000/):
![Home Page](/assets/screenshots/home.png?raw=true "Home Page")

Now enter a valid Youtube Link, select vocal preferences, and click run script! A video will display on the page once code is done running. 

## Example output
Instrumentals + Lyrics: 

https://github.com/huang-kenneth/Karaoke-machine/assets/67389462/362cd9ab-3096-479d-b7cd-e3a37b3d34c6

## Update 9/15/23
Added a front-end GUI using Flask. 
Adjusted code to work with GUI, added new folders and changes output destinations. 

## To do (Mostly UI/Code Cleaning Changes):
  - Make selecting Whisper models easier for users. 
  - Allow users to change the background of video. 
  - Follow words as song progresses (like karaoke videos)
