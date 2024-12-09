from gtts import gTTS
import pygame



def TTS(voice):
    pygame.mixer.init()
    tts = gTTS(text=voice, lang='ko')
    tts.save("helloKr.mp3")

    pygame.mixer.music.load("helloKr.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

    print("complate!")

#TTS("안녕하세요")