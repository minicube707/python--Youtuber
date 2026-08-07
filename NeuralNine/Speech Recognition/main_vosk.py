import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Download the Vosk speech recognition model from:
# https://alphacephei.com/vosk/

# Path to the downloaded Vosk model
MODEL_PATH = "vosk-model-small-en-us-0.15"

# Load the speech recognition model
model = Model(MODEL_PATH)

# Create a recognizer configured for a 16 kHz audio stream
recognizer = KaldiRecognizer(model, 16000)

# Queue used to safely transfer audio data from the callback
# to the main processing loop
q = queue.Queue()


def callback(indata, frames, time, status):
    """
    Audio callback function called automatically by SoundDevice.

    Parameters:
    - indata: Raw audio data captured from the microphone.
    - frames: Number of audio frames.
    - time: Timing information.
    - status: Indicates any audio input errors or warnings.
    """
    # Store the recorded audio bytes in the queue
    q.put(bytes(indata))


# Open the default microphone input stream
with sd.RawInputStream(
    samplerate=16000,   # Audio sample rate (must match the recognizer)
    blocksize=4000,     # Number of samples processed per callback
    dtype="int16",      # 16-bit PCM audio format
    channels=1,         # Mono audio
    callback=callback,  # Function called whenever new audio is available
):
    print("Listening...")

    # Continuously process incoming audio
    while True:
        
        # Wait until a new audio block is available
        data = q.get()

        # Check if the recognizer has detected a complete phrase
        if recognizer.AcceptWaveform(data):
            # Convert the JSON result into a Python dictionary
            result = json.loads(recognizer.Result())

            # Extract the recognized text
            text = result["text"]

            # Print the final recognized sentence if it is not empty
            if text:
                print("\rFinal:", text.lower())

        else:
            # Get the partial (intermediate) recognition result
            partial = json.loads(recognizer.PartialResult())["partial"]

            # Display the partial transcription in real time
            if partial:
                print("\r" + partial, end="", flush=True)