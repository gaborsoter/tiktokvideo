from pydub import AudioSegment

sound = AudioSegment.from_wav("files/garyvee.mp4.wav")
sound = sound.set_channels(1)
sound.export("files/garyvee.mp4mono.wav", format="wav")