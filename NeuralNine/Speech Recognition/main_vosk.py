import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

#Link to download the model
#https://alphacephei.com/vosk/

MODEL_PATH = "vosk-model-small-en-us-0.15"

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)

q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

with sd.RawInputStream(
    samplerate=16000,
    blocksize=4000,
    dtype="int16",
    channels=1,
    callback=callback,
):
    print("Listen...")

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result["text"]

            if text:
                print("\rFinal :", text.lower())
        else:
            partial = json.loads(recognizer.PartialResult())["partial"]
            if partial:
                print("\r" + partial, end="", flush=True)