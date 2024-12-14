import AI_service_call
from AI_service_call import AISpeakerCall
import tmp
import tts
from tmp import control_recording
from keyword_spotting import start_wake_word_detection

AI = AISpeakerCall()
#Detect_command = start_wake_word_detection()

#input = input("AI요청: ")
'''
input = control_recording()
output = AI.process_conversation(input)
'''

#print(output)
def AiCall():
    input = control_recording()
    output = AI.process_conversation(input)

    print(f"response: {output['response']}")
    print(f"action: {output['action']}")
    print(f"device: {output['device']}")
    print(f"value: {output['value']}")
    print(f"status: {output['status']}")

    status = output['status']
    return status


while True:

    Detect_command = start_wake_word_detection()

    if Detect_command is True:
        status = AiCall()
        Detect_command = False

        # if status == "success":
        #     print(f"Detect_command:{Detect_command}")
        #     continue
'''
        else:
            continue

    else:
        continue
'''

"""
while True:
    status = AiCall()2
    

    if status == "success":
        break

    else:
        continue
"""