import AI_service_call
from AI_service_call import AISpeakerCall
#import tmp
#import tts
#from tmp import control_recording
from voiceRec2STT import voice_record_and_transcribe as voice2STT
#from STT import control_recording
#from voiceRec import voice_REC
from keyword_spotting import start_wake_word_detection
from tts import TTS
import openwakeword
#from controlLED import control_led
from openwakeword.model import Model
openwakeword.utils.download_models()



AI = AISpeakerCall()
#Detect_command = start_wake_word_detection()

#input = input("AI요청: ")
'''
input = control_recording()
output = AI.process_conversation(input)
'''

#print(output)
def AiCall():

#    voice_REC()
#    input = control_recording()
    input = voice2STT()
    output = AI.process_conversation(input)

    print(f"response: {output['response']}")
    print(f"action: {output['action']}")
    print(f"device: {output['device']}")
    print(f"value: {output['value']}")
    print(f"status: {output['status']}")

    status = output['status']
#    control_led(output["device"], output["action"])
    TTS(output['response'])

    return status

    

while True:

    Detect_command = start_wake_word_detection()

    if Detect_command is True:
        status = AiCall()
        Detect_command = False

        # if status == "success":
        #     print(f"Detect_command:{Detect_command}")
        #     continue

