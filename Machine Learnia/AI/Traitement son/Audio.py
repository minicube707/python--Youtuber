import pyaudio as pa
import numpy as np

# Fréquence du son en Hz
frequency = 5000

# Durée du son en secondes
duration = 2

# Générer les échantillons
samples = (np.sin(2 * np.pi * np.arange(duration * 44100) * frequency / 44100)).astype(np.float32)

# Initialiser PyAudio
p = pa.PyAudio()

# Ouvrir un flux audio
stream = p.open(format=pa.paFloat32, channels=1, rate=44100, output=True)

# Jouer les échantillons
stream.write(samples.tobytes())

# Fermer le flux audio
stream.stop_stream()
stream.close()

# Terminer PyAudio
p.terminate()
