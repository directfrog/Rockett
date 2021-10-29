import pyaudio
import wave
import time
import pyttsx3

class speech_recog_object(object):
  def __init__(self):
    self.chunk = 1024  # Record in chunks of 1024 samples
    self.sample_format = pyaudio.paInt16  # 16 bits per sample
    self.channels = 1
    self.fs = 44100  # Record at 44100 samples per second
    self.seconds = 5
    self.filename = "output.wav"
    self.p = pyaudio.PyAudio()  # Create an interface to PortAudio
    self.frames = []  # Initialize array to store frames
    self.stream = self.p.open(format=self.sample_format,
                    channels=self.channels,
                    rate=self.fs,
                    frames_per_buffer=self.chunk,
                    input=True)

  def run(self):
    # Store data in chunks for 3 seconds
    tick = 0
    for i in range(0, int(self.fs / self.chunk * self.seconds)):
        self.data = self.stream.read(self.chunk)
        self.frames.append(self.data)
        tick += 1
     
    # Stop and close the stream 
    self.stream.stop_stream()
    self.stream.close()
    # Terminate the PortAudio interface
    self.p.terminate()
    print('Finished listening')
    # Save the recorded data as a WAV file
    self.wf = wave.open(self.filename, 'wb')
    self.wf.setnchannels(self.channels)
    self.wf.setsampwidth(self.p.get_sample_size(self.sample_format))
    self.wf.setframerate(self.fs)
    self.wf.writeframes(b''.join(self.frames))
    self.wf.close()
    import speech_recognition as sr
    self.r = sr.Recognizer()

    self.harvard = sr.AudioFile('output.wav')
    with self.harvard as source:
       self.audio1 = self.r.record(source, duration=4)
       self.audio2 = self.r.record(source, duration=4)
       self.x = self.r.recognize_google(self.audio1, language = 'en', show_all=True)
       if len(self.x) > 0:
        self.transcript = self.x['alternative'][0]['transcript']
       else:
        self.transcript = None
       return self.transcript
