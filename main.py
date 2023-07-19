import pyaudio
import numpy as np
from pydub import AudioSegment
from constants import *
import pygame
import random
import librosa
import time

clock = pygame.time.Clock()
surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

pygame.init()
rect = pygame.Rect(100, 100, 100, 100)


# Load the MP3 file
audio = AudioSegment.from_file("test.wav", format="mp3")
audio_file = librosa.load('test.wav')
y, sr = audio_file
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
# Configure audio stream
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(audio.sample_width),
                channels=audio.channels,
                rate=audio.frame_rate,
                output=True)

# Stream the audio in chunks
chunk_size = 4096   * 2# Adjust this for better performance
# Convert the audio to raw audio data (array of samples)
samples = np.array(audio.get_array_of_samples())

# Split the samples into chunks
start = 0
end = chunk_size * audio.channels
x, y, width, height = 100, 100, 100, 100

def draw():
    surface.fill((0, 0, 0))#background

    pygame.draw.rect(surface, (255, 0, 0), rect)
    pygame.display.flip()



def update():
    global x, y, width, height, rect
    width = random.randint(0, GAME_WIDTH)
    height = random.randint(0, GAME_HEIGHT)
    rect = pygame.Rect(100, 100, width, height)
    rect.center = (GAME_WIDTH // 2, GAME_HEIGHT // 2)


while start < len(samples):
    st = time.time()
    draw()
    update()


    # Take a chunk of audio samples
    chunk = samples[start:end].tobytes()

    # Play the audio chunk
    stream.write(chunk)

    # Move to the next chunk
    start = end
    end += chunk_size * audio.channels
# Close the audio stream
stream.stop_stream()
stream.close()
p.terminate()
