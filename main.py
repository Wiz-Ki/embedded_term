import AI_service_call
from AI_service_call import AISpeakerCall
import tmp
import tts
from tmp import control_recording

AI = AISpeakerCall()
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
    status = AiCall()

    if status == "success":
        break

    else:
        continue
